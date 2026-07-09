"""Per-run harness state, built by folding the SSE event stream.

The same events that drive the live trace panel are also fed to an
EvidenceCollector, which accumulates them into a RunEvidenceState. After the run
finishes, that state is stored in an in-process registry and served read-only by
GET /runs/{run_id}/evidence. The Run Audit panel renders it exactly as stored,
with no extra enrichment.

The point of folding the same events (rather than keeping a separate log) is a
single source of truth: the live trace and the audit are the same data, one
shown as it streams and one summarized afterward, so they cannot disagree.
"""
from pydantic import BaseModel

from app import pricing


class TokenUsage(BaseModel):
    """Token counts for either a single turn or a whole run (the run total is just
    the per-turn counts summed)."""

    input_tokens: int = 0           # prompt tokens sent to the model
    cached_input_tokens: int = 0    # portion of input_tokens served from cache (billed cheaper)
    output_tokens: int = 0          # tokens the model generated; includes reasoning_tokens
    reasoning_tokens: int = 0       # hidden reasoning tokens (a subset of output_tokens)
    total_tokens: int = 0           # input + output, as reported by the API


class SearchEvent(BaseModel):
    """A record of one search the agent ran, kept in the evidence log."""

    search_id: int                  # the search's id (pairs start/complete)
    query: str                      # the query the agent searched for
    mode: str                       # retrieval mode used
    returned_chunk_ids: list[str]   # all chunk_ids this search returned
    new_chunk_ids: list[str]        # subset of the above not seen by any earlier search this run
    result_count: int               # how many chunks were returned


class ReadEvent(BaseModel):
    """A record of one full-chunk read the agent performed, kept in the evidence log."""

    read_id: int                    # the read's id (pairs start/complete)
    chunk_id: str                   # canonical chunk_id that was read
    video_id: str                   # video the chunk belongs to
    start_ts: int                   # chunk start time in seconds
    end_ts: int                     # chunk end time in seconds


class RunProvenance(BaseModel):
    """Which repo snapshot produced the run. git_sha fingerprints every tracked file
    (recipe, tool prompts, loop code) at once and cannot be edited without changing,
    so it is the real identifier; recipe_version rides along as a human label."""

    git_sha: str                    # commit SHA, or a build-time env / "unknown" fallback
    git_dirty: bool                 # True if the working tree had uncommitted changes
    recipe_version: str             # human-friendly label from the recipe frontmatter


class AgentConfig(BaseModel):
    """The effective runtime knobs the run used. These are the values a Phase 6
    ablation varies, recorded verbatim (not versioned) so each run states its own
    conditions. Access/infra gates (spend caps, quotas) are deliberately excluded."""

    model: str                      # settings.agent_model
    exploration_effort: str         # settings.reasoning_effort (search/read turns)
    synthesis_effort: str           # settings.synthesis_reasoning_effort (submit turn)
    max_steps: int                  # settings.agent_max_steps (step budget)
    retrieval_backend: str          # settings.retrieval_backend (pgvector | opensearch)
    retrieval_mode: str             # effective mode (pgvector forces dense)
    retrieval_k: int                # settings.retrieval_k default; model may override per search
    embedding_model: str            # settings.embedding_model
    embedding_dimensions: int       # settings.embedding_dimensions (1536 Matryoshka)
    output_directive: str | None    # channel's appended directive, or None


class RunEvidenceState(BaseModel):
    """The complete harness record for one run: what the agent retrieved, read, and
    cited, plus behavioral metrics, token cost, and the run's outcome. This is what
    the Run Audit panel displays."""

    # --- identity & configuration ---
    run_id: str                     # unique id for this run
    trace_url: str | None           # link to the full Langfuse trace (cost/observability)
    query: str                      # the user's question
    channel: str                    # corpus/channel searched
    recipe_version: str             # prompt recipe version used
    retrieval_mode: str             # bm25 | dense | hybrid
    model: str                      # model that ran the agent

    # --- provenance (which agent, under what conditions) ---
    provenance: RunProvenance       # repo fingerprint + recipe label
    agent_config: AgentConfig       # the effective behavior knobs for this run

    # --- raw activity logs ---
    search_events: list[SearchEvent]   # every search, in order
    read_events: list[ReadEvent]       # every successful read, in order

    # --- derived sets of chunk_ids ---
    seen_chunks: set[str]           # all chunks any search returned
    read_chunks: set[str]           # chunks the agent escalated to a full read
    cited_chunks: set[str]          # chunks referenced in the final answer

    # --- counts (precomputed so the panel does no work) ---
    search_count: int               # number of searches
    read_count: int                 # number of reads
    seen_count: int                 # size of seen_chunks
    cited_count: int                # size of cited_chunks

    # --- behavioral metrics (the "is the harness behaving" signals) ---
    duplicate_search_rate: float            # fraction of searches that returned nothing new
    consecutive_searches_without_read_max: int   # longest run of searches with no read between them
    read_before_cite_violations: list[str]  # chunks cited but never read (snippet-only citations)
    cited_not_seen: list[str]               # chunks cited that no search surfaced; should be empty

    # --- token usage & cost ---
    usage: TokenUsage               # run totals across all turns
    per_turn_usage: list[TokenUsage]   # usage for each turn, in order
    usd_cost: float                 # total cost in USD from the price table
    cost_breakdown: dict            # USD split into input / cached_input / output

    # --- outcome ---
    steps_used: int                 # how many ReAct steps the run took
    budget_exhausted: bool          # True if the run hit the step budget and was forced to answer
    citations_valid: bool           # whether all citations passed index validation


def _chunk_key(video_id: str, start_ts: int) -> str:
    """Build the canonical (zero-padded) chunk_id from a video id and start second,
    matching the format used when chunks were ingested. Used to turn a citation,
    which only has (video_id, start_ts), into the same id space as searches/reads."""
    return f"{video_id}:{int(start_ts):05d}"


class EvidenceCollector:
    """Folds a run's event stream into a RunEvidenceState. Create one per run, feed
    it every event via handle(), then call finalize() once the run succeeds."""

    def __init__(self, *, run_id, query, channel, recipe_version, retrieval_mode,
                 trace_url, model, provenance, agent_config):
        """Store the run's fixed configuration and set up empty accumulators."""
        # fixed config, copied straight into the final state
        self.run_id = run_id
        self.query = query
        self.channel = channel
        self.recipe_version = recipe_version
        self.retrieval_mode = retrieval_mode
        self.trace_url = trace_url
        self.model = model
        self.provenance = provenance      # RunProvenance, built by the caller
        self.agent_config = agent_config  # AgentConfig, built by the caller

        # accumulators, filled in as events arrive
        self.search_events: list[SearchEvent] = []   # one per search_complete
        self.read_events: list[ReadEvent] = []        # one per successful read_complete
        self.seen: set[str] = set()                   # chunk_ids any search has returned
        self.read: set[str] = set()                   # chunk_ids the agent has read in full
        self.per_turn_usage: list[TokenUsage] = []     # one entry per turn_complete

        self._pending_queries: dict[int, str] = {}   # search_id -> query, remembered at search_start
        self._searches_since_read = 0                # running count for the "no read" streak metric
        self._max_searches_without_read = 0          # largest streak seen so far

    def handle(self, event: dict) -> None:
        """Update the running state from one event. Called for every event the run
        emits; ignores event types that don't contribute to the evidence."""
        t = event.get("type")

        if t == "search_start":
            # Remember the query now; we attach it to the record at completion time.
            self._pending_queries[event["search_id"]] = event.get("query", "")

        elif t == "search_complete":
            chunk_ids = event["returned_chunk_ids"]
            new = [c for c in chunk_ids if c not in self.seen]   # chunks not seen before this search
            self.search_events.append(SearchEvent(
                search_id=event["search_id"],
                query=self._pending_queries.pop(event["search_id"], ""),
                mode=self.retrieval_mode,
                returned_chunk_ids=chunk_ids,
                new_chunk_ids=new,
                result_count=event["result_count"],
            ))
            self.seen.update(chunk_ids)
            self._searches_since_read += 1
            self._max_searches_without_read = max(
                self._max_searches_without_read, self._searches_since_read
            )

        elif t == "read_complete":
            if event.get("ok"):   # ignore reads of chunks that weren't found
                self.read_events.append(ReadEvent(
                    read_id=event["read_id"],
                    chunk_id=event["chunk_id"],
                    video_id=event["video_id"],
                    start_ts=event["start_ts"],
                    end_ts=event["end_ts"],
                ))
                self.read.add(event["chunk_id"])
                self._searches_since_read = 0   # a read breaks the search-only streak

        elif t == "turn_complete":
            self.per_turn_usage.append(TokenUsage(**event["usage"]))

    def finalize(self, result) -> RunEvidenceState:
        """Compute the derived sets, metrics, token totals, and cost, and return the
        finished RunEvidenceState. Call once after a successful run; `result` is the
        AgentResult, which supplies the citations and the run outcome."""
        cited = {_chunk_key(c.video_id, c.start_ts) for c in result.citations}

        # Sum per-turn usage into run totals, then price it.
        total = TokenUsage(
            input_tokens=sum(u.input_tokens for u in self.per_turn_usage),
            cached_input_tokens=sum(u.cached_input_tokens for u in self.per_turn_usage),
            output_tokens=sum(u.output_tokens for u in self.per_turn_usage),
            reasoning_tokens=sum(u.reasoning_tokens for u in self.per_turn_usage),
            total_tokens=sum(u.total_tokens for u in self.per_turn_usage),
        )
        usd, breakdown = pricing.cost_usd(
            self.model, total.input_tokens, total.cached_input_tokens, total.output_tokens
        )

        # A search is "redundant" if it returned results but added no new chunks.
        searches_with_results = [s for s in self.search_events if s.result_count > 0]
        redundant = [s for s in searches_with_results if not s.new_chunk_ids]
        dup_rate = (len(redundant) / len(searches_with_results)) if searches_with_results else 0.0

        return RunEvidenceState(
            run_id=self.run_id,
            trace_url=self.trace_url,
            query=self.query,
            channel=self.channel,
            recipe_version=self.recipe_version,
            retrieval_mode=self.retrieval_mode,
            model=self.model,
            provenance=self.provenance,
            agent_config=self.agent_config,
            search_events=self.search_events,
            read_events=self.read_events,
            seen_chunks=self.seen,
            read_chunks=self.read,
            cited_chunks=cited,
            search_count=len(self.search_events),
            read_count=len(self.read_events),
            seen_count=len(self.seen),
            cited_count=len(cited),
            duplicate_search_rate=round(dup_rate, 3),
            consecutive_searches_without_read_max=self._max_searches_without_read,
            read_before_cite_violations=sorted(cited - self.read),
            cited_not_seen=sorted(cited - self.seen),
            usage=total,
            per_turn_usage=self.per_turn_usage,
            usd_cost=round(usd, 6),
            cost_breakdown={k: round(v, 6) for k, v in breakdown.items()},
            steps_used=result.steps_used,
            budget_exhausted=result.budget_exhausted,
            citations_valid=True,   # terminal submit only succeeds when all citations validate
        )


# In-process registry of finished runs. Ephemeral (cleared on restart), which is
# fine for a live demo. Keyed by run_id, with a pointer to the most recent run.
_RUNS: dict[str, RunEvidenceState] = {}
_LATEST: str | None = None


def put_run(state: RunEvidenceState) -> None:
    """Store a finished run's evidence and mark it as the latest."""
    global _LATEST
    _RUNS[state.run_id] = state
    _LATEST = state.run_id


def get_run(run_id: str) -> RunEvidenceState | None:
    """Look up a run's evidence by id, or None if there's no such run."""
    return _RUNS.get(run_id)


def latest_run() -> RunEvidenceState | None:
    """Return the most recently finished run's evidence, or None if none yet."""
    return _RUNS.get(_LATEST) if _LATEST else None
