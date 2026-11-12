"""Ranking and calibration metrics, written out so the math is inspectable."""


def auc(scores: list[float], labels: list[int]) -> float:
    """Probability a random won account outranks a random lost one (ties count half)."""
    pos = [s for s, y in zip(scores, labels) if y == 1]
    neg = [s for s, y in zip(scores, labels) if y == 0]
    if not pos or not neg:
        return 0.5
    wins = sum((p > n) + 0.5 * (p == n) for p in pos for n in neg)
    return wins / (len(pos) * len(neg))


def precision_at(scores: list[float], labels: list[int], frac: float) -> float:
    """Win rate among the top `frac` of accounts by score. Ties broken by input order."""
    k = max(1, round(len(scores) * frac))
    ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
    return sum(labels[i] for i in ranked) / k


def lift_at(scores: list[float], labels: list[int], frac: float) -> float:
    base = sum(labels) / len(labels)
    return precision_at(scores, labels, frac) / base if base else 0.0


def brier(probs: list[float], labels: list[int]) -> float:
    return sum((p - y) ** 2 for p, y in zip(probs, labels)) / len(labels)


def calibration(probs: list[float], labels: list[int], bins: int = 5) -> list[dict]:
    """Equal-count bins: mean predicted probability versus observed win rate."""
    order = sorted(range(len(probs)), key=lambda i: probs[i])
    size = len(order) / bins
    out = []
    for b in range(bins):
        idx = order[round(b * size): round((b + 1) * size)]
        if idx:
            out.append({"bin": b + 1, "n": len(idx),
                        "mean_predicted": round(sum(probs[i] for i in idx) / len(idx), 3),
                        "observed": round(sum(labels[i] for i in idx) / len(idx), 3)})
    return out
