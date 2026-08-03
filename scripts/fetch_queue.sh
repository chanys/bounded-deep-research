#!/bin/bash
# Fetch transcripts for several channels, one at a time, in the order given.
#
# Sequential on purpose: two concurrent scrapers double the request rate against
# YouTube's transcript endpoint, which turns a transient drop into a real block.
#
# Launch detached so it outlives whatever started it, under caffeinate so macOS idle
# sleep does not suspend it mid-run (that cost 72 minutes on the first long run; the
# assertion is released automatically when the queue exits):
#   nohup caffeinate -i bash scripts/fetch_queue.sh starterstory ycombinator_startup_school \
#     > data/fetch_queue.log 2>&1 & disown
#
# For an already-running queue, attach instead of restarting:  caffeinate -i -w <pid> &
#
# Every stage is resumable (fetch_transcripts skips transcripts already on disk),
# so re-running this after an interruption costs nothing for work already done.
#
# Each argument is a channel slug, optionally with a caption language as "slug:lang"
# (default en). A channel whose captions are not in the requested language fails on
# every video, so a non-English channel must say so: kedaibiao:zh
set -u
cd "$(dirname "$0")/.."

for arg in "$@"; do
  channel="${arg%%:*}"
  lang="${arg#*:}"
  [ "$lang" = "$channel" ] && lang=en
  echo "=== $channel (lang=$lang) starting at $(date) ==="
  PYTHONUNBUFFERED=1 uv run python -m ingest.fetch_transcripts \
    --channel "$channel" --lang "$lang" >> "data/${channel}_fetch.log" 2>&1
  status=$?
  n=$(ls "data/transcripts/$channel" 2>/dev/null | wc -l | tr -d ' ')
  echo "=== $channel exited $status at $(date), $n transcripts on disk ==="
done

echo "=== queue finished at $(date) ==="
