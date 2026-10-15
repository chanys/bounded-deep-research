"""In-memory cache of finished answers, keyed by (channel, normalized question).

A repeated question (most often an example-prompt card) replays the original run's
event stream instead of paying for a new agent run. Kept in process memory on
purpose: every deploy starts with an empty cache, so a code, prompt, or model
change can never serve an answer produced by the old version. Entries expire
after TTL so newly ingested videos eventually reach repeated questions.

MAX_ENTRIES bounds memory: one run's events measured ~260 KB as Python objects,
and the daily spend caps allow several hundred fresh runs a day, so a week of
unique questions could otherwise approach the ECS task's 1 GB. 500 entries is
~130 MB at most.
"""
import re
import time

TTL_SECONDS = 7 * 24 * 3600
MAX_ENTRIES = 500

_CACHE: dict[tuple[str, str], tuple[float, list[dict]]] = {}


def normalize(query: str) -> str:
    """Casefold, collapse whitespace, and drop trailing punctuation, so trivially
    different spellings of the same question share one entry."""
    q = re.sub(r"\s+", " ", query).strip().casefold()
    return q.rstrip("?？.。!！ ")


def get(channel: str, query: str) -> list[dict] | None:
    """The recorded events of a fresh cached run for this question, or None."""
    entry = _CACHE.get((channel, normalize(query)))
    if entry is None or time.time() - entry[0] > TTL_SECONDS:
        return None
    return entry[1]


def put(channel: str, query: str, events: list[dict]) -> None:
    """Store a successful run's events. Drops expired entries, then the oldest
    ones beyond MAX_ENTRIES (dicts keep insertion order, oldest first)."""
    now = time.time()
    for key in [k for k, (ts, _) in _CACHE.items() if now - ts > TTL_SECONDS]:
        del _CACHE[key]
    key = (channel, normalize(query))
    _CACHE.pop(key, None)   # re-insert at the end so its age order stays correct
    _CACHE[key] = (now, events)
    while len(_CACHE) > MAX_ENTRIES:
        del _CACHE[next(iter(_CACHE))]
