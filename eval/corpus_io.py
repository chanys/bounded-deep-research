"""Shared corpus IO + population reconciliation for the code4AI eval (Stage 1).

Scope is the code4AI channel only. The answerable population is the set of
videos that have a cleaned transcript on disk AND a manifest record (475 today,
versus 1338 in the manifest, since only 475 have been transcribed). reconcile()
cross-checks the manifest, the transcript files, and the DB chunk counts and
fails loudly on a boundary mismatch, so a half-loaded corpus can't silently
skew the inventory.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from core.db import transaction

CHANNEL = "code4AI"
MANIFEST = Path("data/channel_manifests/code4AI.jsonl")
CLEAN_DIR = Path("data/transcripts_clean/code4AI")


def load_manifest() -> dict[str, dict]:
    """video_id -> manifest record, for every manifest video (not just transcribed)."""
    records: dict[str, dict] = {}
    for ln in MANIFEST.read_text().splitlines():
        ln = ln.strip()
        if not ln:
            continue
        rec = json.loads(ln)
        records[rec["id"]] = rec
    return records


def transcript_ids() -> set[str]:
    """Video ids that have a cleaned transcript on disk (the *.jsonl stems)."""
    return {p.stem for p in CLEAN_DIR.glob("*.jsonl")}


def read_summaries(path: Path) -> dict[str, dict]:
    """video_id -> summary record from a Stage A JSONL (skips the _meta header line)."""
    if not path.exists():
        return {}
    out: dict[str, dict] = {}
    for ln in path.read_text().splitlines():
        ln = ln.strip()
        if not ln:
            continue
        obj = json.loads(ln)
        if "_meta" in obj:
            continue
        out[obj["video_id"]] = obj
    return out


def load_transcript(video_id: str) -> tuple[dict, list[dict]]:
    """Return (meta_header, segments) for a cleaned transcript.

    Line 0 is a {"_meta": {...}} header; lines 1+ are {"text","start","duration"}.
    """
    lines = (CLEAN_DIR / f"{video_id}.jsonl").read_text().splitlines()
    meta = json.loads(lines[0]).get("_meta", {})
    segments = [json.loads(ln) for ln in lines[1:] if ln.strip()]
    return meta, segments


def transcript_text(video_id: str) -> str:
    """Full cleaned transcript as one string (segment texts joined by spaces)."""
    _meta, segments = load_transcript(video_id)
    return " ".join(seg["text"].strip() for seg in segments if seg.get("text"))


def read_inventory(path: Path) -> dict:
    """Load the machine-readable inventory JSON produced by build_inventory."""
    return json.loads(path.read_text())


def video_chunks(video_id: str) -> list[dict]:
    """Ordered DB chunks for one video: [{chunk_id, start_s, end_s, text}, ...].

    chunk_id is the DB primary key `video_id:start_s` (zero-padded), which is also
    the retrieval join key. Raises if the DB is down.
    """
    sql = (
        "SELECT chunk_id, start_s, end_s, text "
        "FROM video_chunks WHERE video_id = %s ORDER BY start_s"
    )
    with transaction() as conn:
        rows = conn.execute(sql, (video_id,)).fetchall()
    return [dict(r) for r in rows]


def db_chunk_counts() -> dict[str, int]:
    """video_id -> chunk count for the channel, from Postgres. Raises if the DB is down."""
    sql = (
        "SELECT c.video_id, COUNT(*) AS n "
        "FROM video_chunks c JOIN videos v USING (video_id) "
        "WHERE v.channel = %s GROUP BY c.video_id"
    )
    with transaction() as conn:
        rows = conn.execute(sql, (CHANNEL,)).fetchall()
    return {r["video_id"]: r["n"] for r in rows}


class BoundaryError(RuntimeError):
    """A corpus population mismatch that must stop the run rather than skew results."""


@dataclass
class Scope:
    manifest: dict[str, dict]
    population: list[str]           # sorted ids = manifest ∩ transcripts
    chunk_counts: dict[str, int]    # video_id -> n (empty when require_db=False)
    warnings: list[str] = field(default_factory=list)


def population() -> list[str]:
    """The sorted answerable ids (manifest ∩ transcripts). No DB required."""
    return sorted(transcript_ids() & set(load_manifest()))


def reconcile(*, require_db: bool = True) -> Scope:
    """Cross-check manifest / transcripts / DB and return the frozen population.

    Raises BoundaryError when a transcript lacks metadata, or (require_db) when a
    transcribed video is missing from the DB. A DB-only video is a warning.
    """
    manifest = load_manifest()
    tids = transcript_ids()
    manifest_ids = set(manifest)

    orphans = tids - manifest_ids
    if orphans:
        raise BoundaryError(
            f"{len(orphans)} transcript(s) have no manifest record, "
            f"e.g. {sorted(orphans)[:5]}"
        )

    pop = sorted(tids & manifest_ids)
    warnings: list[str] = []
    chunk_counts: dict[str, int] = {}

    if require_db:
        chunk_counts = db_chunk_counts()
        missing = [vid for vid in pop if vid not in chunk_counts]
        if missing:
            raise BoundaryError(
                f"{len(missing)} transcribed video(s) are missing from the DB "
                f"(corpus not fully loaded). Load it: `make up`, then "
                f"`PGPASSWORD=... make corpus-restore`, then `make smoke`. "
                f"e.g. {missing[:5]}"
            )
        pop_set = set(pop)
        extra = [vid for vid in chunk_counts if vid not in pop_set]
        if extra:
            warnings.append(
                f"{len(extra)} video(s) in the DB but not in the transcript set (ignored)"
            )

    return Scope(manifest=manifest, population=pop, chunk_counts=chunk_counts, warnings=warnings)
