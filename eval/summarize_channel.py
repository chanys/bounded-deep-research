"""Per-video summaries + key points for any channel, incrementally and resumably.

A standalone reading tool: fetch a channel's transcripts, summarize each video, and
read the summaries instead of watching hours of video. Output is not corpus data and
does not feed the agent, so nothing here runs clean_transcripts / chunking / embedding.

The prompt is deliberately a separate copy from eval.summarize_transcripts rather than
an import. That module's prompt is part of the frozen Phase 4 instrument, and this one
diverges from it (inline ASR correction), so sharing would either contaminate a
calibrated measurement or drift from it silently.

Because it reads raw ASR, the prompt asks for mis-transcriptions to be corrected inline
and reported in asr_corrections. Names and terms only: a numeric value that was misheard
cannot be recovered from context, and a confident-looking wrong number is worse than a
visibly odd one, so figures are always left as spoken.

Usage:
  uv run python -m eval.summarize_channel --channel starterstory --limit 3   # smoke
  uv run python -m eval.summarize_channel --channel starterstory             # rest
  uv run python -m eval.summarize_channel --channel starterstory --redo      # ignore existing
"""
from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from pydantic import BaseModel
from tqdm import tqdm

from core.claude_llm import call_structured, enable_usage_capture, usage_totals
from core.provenance import PROVENANCE

MODEL = "claude-sonnet-5"
PROMPT_VERSION = "summarize-channel-v1.2-asr-lang"

# Appended when --output-language is given, mirroring how app/channels.py steers a
# channel's output language without forking the shared prompt. Only the model's own
# prose is translated: creator_questions are extracted verbatim and entities are proper
# nouns, so translating either would corrupt them.
OUTPUT_DIRECTIVE = (
    "\n\nWrite summary, key_points, and topics in {language}. Leave creator_questions "
    "verbatim in the language spoken, and leave entities in the form they appear in "
    "(do not translate product, company, or personal names)."
)

# Higher than the code4AI pass's 3000: these channels run to 80-minute interviews,
# and a truncated response parses to None and loses the whole (paid) call.
MAX_TOKENS = 8000

# Sonnet 5 list price, USD per million tokens, for the pre-spend estimate only.
USD_IN_PER_M = 3.0
USD_OUT_PER_M = 15.0
EST_OUT_TOKENS = 1900  # measured over the starterstory smoke; an initial guess of 700 was 2x low

SYSTEM = (
    "You summarize a single YouTube video from its transcript, so a reader can skip watching "
    "it. Be faithful to what is actually said; do not invent facts, and do not judge quality. "
    "Return structured data only.\n\n"
    "The transcript is auto-generated speech recognition and contains transcription errors, "
    "especially on proper nouns: product names, companies, people, and technical terms. Silently "
    "correct these in your output when context makes the intended term clear (for example a "
    "transcript reading 'Cloud Code' in a discussion of AI developer tools means 'Claude Code'). "
    "Apply the same correction consistently everywhere it appears, and list what you corrected "
    "in asr_corrections.\n\n"
    "Two limits on this. Correct only when you are confident from context or well-known usage; "
    "if a garbled term is genuinely ambiguous, keep it as transcribed rather than guessing. And "
    "never alter numbers, quantities, dates, or monetary amounts: a misheard figure cannot be "
    "recovered from context, so report figures exactly as spoken even when one looks implausible."
)

USER_TEMPLATE = (
    "Video title: {title}\n\n"
    "Transcript:\n{text}\n\n"
    "Produce:\n"
    "- summary: 2-4 sentences on what this video actually covers.\n"
    "- key_points: the concrete claims, findings, numbers, or results the video actually "
    "asserts, each a short standalone statement specific enough to be useful on its own. "
    "Capture the substantive points, not every minor detail.\n"
    "- topics: the main topics/themes discussed, as short phrases.\n"
    "- entities: specific products, companies, tools, techniques, or people named.\n"
    "- creator_questions: questions the creator explicitly poses or asks aloud in the "
    "transcript, extracted verbatim (light cleanup of ASR errors is fine). Include EVERY "
    "one you find; do not filter for quality or interestingness. Empty list if none.\n"
    "- asr_corrections: each transcription error you corrected, as 'as transcribed -> "
    "corrected'. Empty list if none."
)


class VideoSummary(BaseModel):
    summary: str
    key_points: list[str]
    topics: list[str]
    entities: list[str]
    creator_questions: list[str]
    asr_corrections: list[str]


def out_path(channel: str) -> Path:
    return Path(f"data/summaries/{channel}.jsonl")


def read_existing(path: Path) -> dict[str, dict]:
    """video_id -> record from a summaries JSONL, skipping the _meta header line."""
    if not path.exists():
        return {}
    out = {}
    for ln in path.read_text().splitlines():
        if ln.strip():
            obj = json.loads(ln)
            if "_meta" not in obj:
                out[obj["video_id"]] = obj
    return out


def load_manifest(channel: str) -> dict[str, dict]:
    """video_id -> manifest record for one channel."""
    path = Path(f"data/channel_manifests/{channel}.jsonl")
    if not path.exists():
        raise SystemExit(f"no manifest at {path}; run ingest.list_channel_videos first")
    records = {}
    for ln in path.read_text().splitlines():
        if ln.strip():
            rec = json.loads(ln)
            records[rec["id"]] = rec
    return records


def est_tokens(text: str) -> int:
    """Rough input-token count, counting CJK separately.

    A CJK character is worth about a whole token, where English averages ~4 chars per
    token. Using one ratio for both understated a Chinese channel's cost by 4x, which
    defeats the point of a pre-spend estimate.
    """
    cjk = sum(1 for ch in text if "一" <= ch <= "鿿" or "぀" <= ch <= "ヿ")
    return int(cjk + (len(text) - cjk) / 4)


def transcript_text(path: Path) -> str:
    """Full transcript as one string; line 0 is the _meta header, lines 1+ are segments."""
    lines = path.read_text().splitlines()
    segs = [json.loads(ln) for ln in lines[1:] if ln.strip()]
    return " ".join(s["text"].strip() for s in segs if s.get("text"))


# Sentence-final punctuation, including the full-width CJK forms. Without the CJK
# characters every Chinese summary would look truncated and be dropped.
TERMINAL_PUNCT = (".", "!", "?", "。", "！", "？", "…", "”", '"', "'", "」", "』")


def degenerate_reason(out: VideoSummary) -> str | None:
    """Why this response is a stub rather than a real summary, or None if it looks real.

    Seen intermittently: the model stops early, leaving the summary cut off mid-sentence
    and every list holding a literal "placeholder". The schema is satisfied, so nothing
    raises - it has to be caught on content. Retrying the same video cleared it 3/3 in
    testing, so this is sampling noise rather than something to prompt away.
    """
    stubs = (*out.key_points, *out.topics, *out.entities, *out.asr_corrections)
    if any(s.strip().lower() == "placeholder" for s in stubs):
        return "placeholder list entries"
    if not out.summary.rstrip().endswith(TERMINAL_PUNCT):
        return "summary ends mid-sentence"
    if not out.key_points:
        return "no key points"
    return None


async def summarize_one(vid: str, rec: dict, text: str, sem: asyncio.Semaphore,
                        language: str | None = None, attempts: int = 3) -> dict | None:
    """Summarize one video; returns None on failure so one bad call cannot kill the batch."""
    system = SYSTEM + (OUTPUT_DIRECTIVE.format(language=language) if language else "")
    async with sem:
        for attempt in range(attempts):
            try:
                out = await call_structured(
                    system,
                    USER_TEMPLATE.format(title=rec.get("title", ""), text=text),
                    VideoSummary,
                    model=MODEL,
                    max_tokens=MAX_TOKENS,
                    thinking={"type": "disabled"},
                )
            except Exception as e:  # noqa: BLE001 - keep the batch alive
                print(f"  fail {vid}: {type(e).__name__}: {e}", flush=True)
                return None
            reason = degenerate_reason(out)
            if reason is None:
                break
            print(f"  retry {vid}: {reason} (attempt {attempt + 1}/{attempts})", flush=True)
        else:
            print(f"  drop {vid}: still degenerate after {attempts} attempts", flush=True)
            return None
    return {
        "video_id": vid,
        "url": f"https://www.youtube.com/watch?v={vid}",
        "title": rec.get("title", ""),
        "published_at": rec.get("publishedAt"),
        "duration_seconds": rec.get("duration_seconds"),
        "summary": out.summary,
        "key_points": out.key_points,
        "topics": out.topics,
        "entities": out.entities,
        "creator_questions": out.creator_questions,
        "asr_corrections": out.asr_corrections,
        "model": MODEL,
        "prompt_version": PROMPT_VERSION,
        "output_language": language,
    }


async def amain(args: argparse.Namespace) -> None:
    channel = args.channel
    manifest = load_manifest(channel)
    tdir = Path(f"data/transcripts/{channel}")
    if not tdir.is_dir():
        raise SystemExit(f"no transcripts at {tdir}")

    on_disk = {p.stem: p for p in sorted(tdir.glob("*.jsonl"))}
    orphans = set(on_disk) - set(manifest)
    if orphans:
        raise SystemExit(f"{len(orphans)} transcript(s) have no manifest record, e.g. {sorted(orphans)[:5]}")

    out = out_path(channel)
    existing = {} if args.redo else read_existing(out)
    todo = [v for v in sorted(on_disk) if v not in existing]
    if args.limit:
        todo = todo[: args.limit]

    print(f"channel={channel} on_disk={len(on_disk)} existing={len(existing)} "
          f"to_summarize={len(todo)}", flush=True)
    if not todo:
        print("nothing to do", flush=True)
        return

    texts = {v: transcript_text(on_disk[v]) for v in todo}
    in_tok = sum(est_tokens(t) for t in texts.values())
    est = (in_tok / 1e6) * USD_IN_PER_M + (len(todo) * EST_OUT_TOKENS / 1e6) * USD_OUT_PER_M
    print(f"estimated spend: ~${est:.2f} ({in_tok/1000:.0f}k input tokens, {len(todo)} calls)", flush=True)

    enable_usage_capture()
    out.parent.mkdir(parents=True, exist_ok=True)
    new_file = not out.exists()
    sem = asyncio.Semaphore(args.concurrency)
    tasks = [summarize_one(v, manifest[v], texts[v], sem, args.output_language) for v in todo]

    # Append as each call returns: an interrupted run keeps everything already paid for.
    written = 0
    with out.open("a", encoding="utf-8") as f:
        if new_file:
            f.write(json.dumps({"_meta": {
                "channel": channel,
                "model": MODEL,
                "prompt_version": PROMPT_VERSION,
                "output_language": args.output_language,
                "thinking": "disabled",
                "transcript_source": "raw ASR, corrected inline by the summarizer",
                "provenance": {"git_sha": PROVENANCE.git_sha, "git_dirty": PROVENANCE.git_dirty},
            }}, ensure_ascii=False) + "\n")
        for coro in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc=channel):
            rec = await coro
            if rec:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                f.flush()
                written += 1

    usage = usage_totals()
    print(f"done: +{written} summaries ({len(todo) - written} failed) -> {out}", flush=True)
    if usage:
        actual = (usage["input_tokens"] / 1e6) * USD_IN_PER_M + (usage["output_tokens"] / 1e6) * USD_OUT_PER_M
        print(f"actual spend: ${actual:.2f} "
              f"(in={usage['input_tokens']:,} out={usage['output_tokens']:,})", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--channel", required=True)
    ap.add_argument("--output-language", default=None,
                    help="write summary/key_points/topics in this language, e.g. Chinese "
                         "(default: whatever the transcript is in)")
    ap.add_argument("--limit", type=int, default=None, help="only the first N pending (smoke)")
    ap.add_argument("--redo", action="store_true", help="ignore existing summaries")
    ap.add_argument("--concurrency", type=int, default=6)
    asyncio.run(amain(ap.parse_args()))


if __name__ == "__main__":
    main()
