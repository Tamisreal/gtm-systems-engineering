"""Metric math, kept separate from I/O so it can be unit tested on hand-made cases."""

from collections import defaultdict

NEGATION_WORDS = (" not ", " never ", " no ", " ignore")


def prf(tp: int, fp: int, fn: int) -> dict:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"tp": tp, "fp": fp, "fn": fn,
            "precision": round(precision, 3), "recall": round(recall, 3), "f1": round(f1, 3)}


def score(predictions: dict[str, list[dict]], truth: dict[str, list[dict]]) -> dict:
    """Compare predicted (type, value) pairs per call with ground truth.

    predictions / truth: {call_id: [{"type", "value", ...}, ...]}
    Returns per-type and micro/macro precision, recall, F1, plus classified failures.
    """
    counts: dict[str, dict[str, int]] = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0})
    failures: list[dict] = []

    for call_id in sorted(set(truth) | set(predictions)):
        true_pairs = {(t["type"], t["value"]) for t in truth.get(call_id, [])}
        preds = {(p["type"], p["value"]): p for p in predictions.get(call_id, [])}
        true_types = {t for t, _ in true_pairs}
        pred_types = {t for t, _ in preds}

        for pair, pred in preds.items():
            if pair in true_pairs:
                counts[pair[0]]["tp"] += 1
                continue
            counts[pair[0]]["fp"] += 1
            evidence = f" {pred.get('evidence', '').lower()} "
            if pair[0] in true_types:
                reason = "wrong_value"
            elif any(w in evidence for w in NEGATION_WORDS):
                reason = "negation_or_context"
            else:
                reason = "spurious"
            failures.append({"call_id": call_id, "kind": "false_positive", "type": pair[0],
                             "value": pair[1], "reason": reason, "evidence": pred.get("evidence")})

        for pair in true_pairs - set(preds):
            counts[pair[0]]["fn"] += 1
            reason = "wrong_value" if pair[0] in pred_types else "missed"
            failures.append({"call_id": call_id, "kind": "false_negative", "type": pair[0],
                             "value": pair[1], "reason": reason})

    per_type = {t: prf(**c) for t, c in sorted(counts.items())}
    total = {k: sum(c[k] for c in counts.values()) for k in ("tp", "fp", "fn")}
    macro_f1 = sum(v["f1"] for v in per_type.values()) / len(per_type) if per_type else 0.0
    return {"micro": prf(**total), "macro_f1": round(macro_f1, 3),
            "per_type": per_type, "failures": failures}


def cost_usd(input_tokens: int, output_tokens: int, price: dict) -> float:
    """price: {"input_per_mtok": float, "output_per_mtok": float}"""
    return (input_tokens * price["input_per_mtok"] + output_tokens * price["output_per_mtok"]) / 1_000_000


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    k = (len(ordered) - 1) * pct
    lo, hi = int(k), min(int(k) + 1, len(ordered) - 1)
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (k - lo)
