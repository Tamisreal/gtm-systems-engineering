"""Train, compare, check for leakage, score the pool and build the outreach queue."""

import csv
import json
from pathlib import Path

from .data import CORE_INDUSTRIES, generate, split
from .evaluate import auc, brier, calibration, lift_at, precision_at
from .features import Standardizer, encode, feature_names
from .models import Lookalike, LogisticRegression, RuleICP
from .outreach import build_queue

RESULTS = Path(__file__).resolve().parent.parent / "results"

# The written ICP a team would start with. It names two of the three core industries,
# which is realistic: a static ICP is usually close, not exact.
WRITTEN_ICP = {"logistics", "manufacturing"}


def _ranking(scores: list[float], labels: list[int]) -> dict:
    return {"auc": round(auc(scores, labels), 3),
            "precision_top10": round(precision_at(scores, labels, 0.10), 3),
            "lift_top10": round(lift_at(scores, labels, 0.10), 2),
            "lift_top20": round(lift_at(scores, labels, 0.20), 2)}


def run(write: bool = True) -> dict:
    accounts = generate()
    train, test, pool = split(accounts)
    y_train = [int(a["won"]) for a in train]
    y_test = [int(a["won"]) for a in test]

    names = feature_names()
    std = Standardizer().fit([encode(a) for a in train])
    X_train, X_test, X_pool = (std.transform([encode(a) for a in rows]) for rows in (train, test, pool))

    rule_scores = RuleICP(WRITTEN_ICP).score(test)
    look = Lookalike(k=10).fit(X_train, y_train, [a["account_id"] for a in train])
    look_scores = look.score(X_test)
    lr = LogisticRegression().fit(X_train, y_train)
    lr_probs = lr.predict_proba(X_test)

    # Leakage trap: add a field recorded after first touch.
    std_leak = Standardizer().fit([encode(a, True) for a in train])
    leaky = LogisticRegression().fit(std_leak.transform([encode(a, True) for a in train]), y_train)
    leaky_test = leaky.predict_proba(std_leak.transform([encode(a, True) for a in test]))
    leaky_pool = leaky.predict_proba(std_leak.transform([encode(a, True) for a in pool]))

    pool_probs = lr.predict_proba(X_pool)
    reasons = [lr.contributions(x, names) for x in X_pool]
    handoff = build_queue(pool, pool_probs, reasons)

    top_weights = sorted(zip(names, lr.w), key=lambda t: abs(t[1]), reverse=True)[:6]
    summary = {
        "label": "SYNTHETIC DEMONSTRATION: invented accounts with a hidden pattern. Not a production result.",
        "data": {"train": len(train), "test": len(test), "pool": len(pool),
                 "train_win_rate": round(sum(y_train) / len(y_train), 3),
                 "test_win_rate": round(sum(y_test) / len(y_test), 3),
                 "split": "time-based: first touch before 2026-04-01 trains, on or after tests"},
        "hidden_core_industries": sorted(CORE_INDUSTRIES),
        "models_on_test": {
            "rule_icp": _ranking(rule_scores, y_test),
            "lookalike_knn": _ranking(look_scores, y_test),
            "logistic_regression": _ranking(lr_probs, y_test) | {"brier": round(brier(lr_probs, y_test), 4)},
        },
        "calibration_logistic": calibration(lr_probs, y_test),
        "top_weights": [(n, round(w, 2)) for n, w in top_weights],
        "leakage_trap": {
            "test_auc_with_meetings_held": round(auc(leaky_test, y_test), 3),
            "pool_score_spread_with_meetings_held": round(max(leaky_pool) - min(leaky_pool), 3),
            "pool_score_spread_without": round(max(pool_probs) - min(pool_probs), 3),
            "note": "meetings_held is 0 for every uncontacted account, so the leaky model's test score says nothing about the pool.",
        },
        "outreach": {
            "queued": len(handoff["queue"]),
            "by_tier": {t: sum(1 for r in handoff["queue"] if r["tier"] == t) for t in "ABC"},
            "holdout": len(handoff["holdout"]),
            "suppressed": len(handoff["suppressed"]),
            "no_outreach": handoff["no_outreach"],
            "send_days": max((r["send_day"] for r in handoff["queue"]), default=0),
        },
    }
    if write:
        RESULTS.mkdir(exist_ok=True)
        (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        with (RESULTS / "outreach_queue.csv").open("w", newline="", encoding="utf-8") as fh:
            cols = ["account_id", "name", "tier", "win_probability", "why", "first_line_signal",
                    "play", "channel", "review", "status", "send_day"]
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            for r in handoff["queue"]:
                w.writerow({**r, "why": "; ".join(r["why"])})
    return summary | {"_handoff": handoff}


def main() -> None:
    s = run()
    print(s["label"])
    print("data:", s["data"])
    for name, m in s["models_on_test"].items():
        print(f"{name:<20} {m}")
    print("calibration (logistic, test):", s["calibration_logistic"])
    print("largest weights:", s["top_weights"])
    print("leakage trap:", {k: v for k, v in s["leakage_trap"].items() if k != "note"})
    print("outreach:", s["outreach"])
    for row in s["_handoff"]["queue"][:3]:
        print("  ", row["tier"], row["account_id"], row["win_probability"], row["why"], "|", row["first_line_signal"])
