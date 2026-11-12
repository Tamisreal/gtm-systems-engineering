"""Confidence routing: what gets written automatically, what a person reviews, what is dropped.

The thresholds are a policy, not a model property. Start conservative, then move
them using reviewer decisions: if reviewers accept 98% of the 0.6-0.8 band for a
signal type, that band can be promoted to auto-apply for that type.
"""

from .vocab import HIGH_IMPACT_TYPES

AUTO_APPLY_MIN = 0.8
REVIEW_MIN = 0.5


def route(signal: dict) -> str:
    conf = float(signal["confidence"])
    if conf < REVIEW_MIN:
        return "drop"
    if signal["type"] in HIGH_IMPACT_TYPES:
        return "review"
    return "auto" if conf >= AUTO_APPLY_MIN else "review"


def route_all(signals: list[dict]) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {"auto": [], "review": [], "drop": []}
    for s in signals:
        out[route(s)].append(s)
    return out
