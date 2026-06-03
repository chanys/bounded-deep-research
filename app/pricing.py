"""Token pricing for the agent models. USD per 1,000,000 tokens.

Cost is computed locally (not fetched from Langfuse) so the Run Audit panel can
render synchronously right after a run. The Langfuse trace_url remains the
authoritative cross-check. Query-embedding cost is treated as negligible.
"""

# USD per 1M tokens. Update when prices change.
MODEL_PRICES: dict[str, dict[str, float]] = {
    "gpt-5.4":      {"input": 2.50, "cached_input": 0.25, "output": 15.0},
    "gpt-5.4-mini": {"input": 0.75, "cached_input": 0.075, "output": 4.5},
}


def cost_usd(model: str, input_tokens: int, cached_input_tokens: int, output_tokens: int) -> tuple[float, dict]:
    """Return (total_usd, breakdown). breakdown has per-bucket USD.

    input_tokens is the full prompt count and *includes* cached tokens, so we
    bill the uncached remainder at the input rate and the cached portion at the
    cheaper cached rate. Reasoning tokens are already part of output_tokens, so
    they're billed there (no separate line).
    """
    p = MODEL_PRICES.get(model)
    if p is None:
        return 0.0, {}
    uncached_input = max(0, input_tokens - cached_input_tokens)
    breakdown = {
        "input": uncached_input / 1e6 * p["input"],
        "cached_input": cached_input_tokens / 1e6 * p["cached_input"],
        "output": output_tokens / 1e6 * p["output"],
    }
    return sum(breakdown.values()), breakdown
