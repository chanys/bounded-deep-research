"""Small statistics helpers for eval scoring (kept dependency-free)."""
from __future__ import annotations


def cohen_kappa(a: list[bool], b: list[bool]) -> float:
    """Cohen's kappa for two binary labelings of the same items.

    kappa = (po - pe) / (1 - pe), where po is observed agreement and pe is the
    agreement expected from the raters' marginal rates by chance. 1.0 = perfect,
    0 = chance-level, negative = worse than chance. Returns 1.0 when both raters
    are constant and identical (pe == 1 and they agree), else 0.0 for that edge.
    """
    if len(a) != len(b) or not a:
        raise ValueError("kappa needs two equal-length non-empty labelings")
    n = len(a)
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    pa = sum(1 for x in a if x) / n
    pb = sum(1 for x in b if x) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    if pe == 1.0:
        return 1.0 if po == 1.0 else 0.0
    return (po - pe) / (1 - pe)
