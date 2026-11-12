"""Run an extractor over the labeled calls and report quality, routing, latency and cost.

Usage (from projects/ai-evaluation):
    python -m evalkit.run_eval                    # rules baseline, no credentials needed
    python -m evalkit.run_eval --extractor llm    # Claude extractor, spends API credits

Writes results/<extractor>_summary.json (committed, so changes show up in review)
and results/<extractor>_log.jsonl (one line per call: raw output, errors, telemetry).
"""

import argparse
import json
import sys
import time
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE.parent / "conversation-intelligence"))

from ci import llm, rules  # noqa: E402
from ci.pipeline import load_calls  # noqa: E402
from ci.route import route_all  # noqa: E402
from ci.validate import split_valid  # noqa: E402

from .metrics import cost_usd, percentile, score  # noqa: E402

TRUTH = HERE / "data" / "ground_truth.json"
PRICING = HERE / "pricing.json"
RESULTS = HERE / "results"


def run(extractor: str = "rules", write: bool = True) -> dict:
    calls = load_calls()
    truth = json.loads(TRUTH.read_text(encoding="utf-8"))["labels"]
    pricing = json.loads(PRICING.read_text(encoding="utf-8"))

    kept, auto_only, log = {}, {}, []
    raw_total = valid_total = 0
    routed_totals = {"auto": 0, "review": 0, "drop": 0}
    rejection_codes: dict[str, int] = {}
    latencies, in_tok, out_tok, call_errors = [], 0, 0, 0

    for call in calls:
        started = time.perf_counter()
        if extractor == "llm":
            raw, telemetry = llm.extract(call)
        else:
            raw, telemetry = rules.extract(call), {}
        latency_ms = telemetry.get("latency_ms", (time.perf_counter() - started) * 1000)
        latencies.append(latency_ms)
        in_tok += telemetry.get("input_tokens", 0)
        out_tok += telemetry.get("output_tokens", 0)
        call_errors += 1 if telemetry.get("error") else 0

        valid, rejected = split_valid(raw, call)
        for r in rejected:
            for code in r["errors"]:
                rejection_codes[code] = rejection_codes.get(code, 0) + 1
        routed = route_all(valid)
        for k, v in routed.items():
            routed_totals[k] += len(v)
        raw_total += len(raw)
        valid_total += len(valid)
        kept[call["call_id"]] = routed["auto"] + routed["review"]
        auto_only[call["call_id"]] = routed["auto"]
        log.append({"call_id": call["call_id"], "raw": raw, "rejected": rejected,
                    "routed": routed, "telemetry": telemetry})

    quality = score(kept, truth)
    auto_quality = score(auto_only, truth)["micro"]
    kept_total = routed_totals["auto"] + routed_totals["review"]
    price = pricing["models"].get(llm.MODEL) if extractor == "llm" else None
    total_cost = cost_usd(in_tok, out_tok, price) if price else 0.0
    tp = quality["micro"]["tp"]

    summary = {
        "label": "SYNTHETIC DEMONSTRATION: 12 invented calls, 57 hand labels. Not a production result.",
        "extractor": extractor,
        "run_date": date.today().isoformat(),
        "calls": len(calls),
        "truth_labels": sum(len(v) for v in truth.values()),
        "quality_kept": quality["micro"] | {"macro_f1": quality["macro_f1"]},
        "quality_auto_applied": auto_quality,
        "per_type": quality["per_type"],
        "structure": {
            "raw_signals": raw_total,
            "schema_and_grounding_valid_rate": round(valid_total / raw_total, 3) if raw_total else 0.0,
            "rejection_codes": rejection_codes,
            "calls_with_errors": call_errors,
        },
        "routing": routed_totals | {"review_share_of_kept": round(routed_totals["review"] / kept_total, 3) if kept_total else 0.0},
        "latency_ms": {"p50": round(percentile(latencies, 0.5), 2), "p95": round(percentile(latencies, 0.95), 2)},
        "cost": {
            "input_tokens": in_tok,
            "output_tokens": out_tok,
            "total_usd": round(total_cost, 4),
            "usd_per_call": round(total_cost / len(calls), 5) if calls else 0.0,
            "usd_per_correct_signal": round(total_cost / tp, 5) if tp else None,
            "pricing_as_of": pricing["as_of"] if price else None,
        },
        "failures": quality["failures"],
    }

    if not write:
        return summary
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / f"{extractor}_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    with (RESULTS / f"{extractor}_log.jsonl").open("w", encoding="utf-8") as fh:
        for row in log:
            fh.write(json.dumps(row) + "\n")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--extractor", choices=["rules", "llm"], default="rules")
    args = parser.parse_args()
    if args.extractor == "llm" and not llm.available():
        raise SystemExit("Install the anthropic package and set credentials to use --extractor llm.")

    s = run(args.extractor)
    q, a = s["quality_kept"], s["quality_auto_applied"]
    print(s["label"])
    print(f"extractor={s['extractor']} calls={s['calls']} labels={s['truth_labels']}")
    print(f"kept (auto+review): P={q['precision']} R={q['recall']} F1={q['f1']} macroF1={q['macro_f1']}")
    print(f"auto-applied only:  P={a['precision']} R={a['recall']} F1={a['f1']}")
    print(f"valid rate={s['structure']['schema_and_grounding_valid_rate']} routing={s['routing']}")
    print(f"latency p50={s['latency_ms']['p50']}ms p95={s['latency_ms']['p95']}ms cost=${s['cost']['total_usd']}")
    print("per type F1:", {t: v["f1"] for t, v in s["per_type"].items()})
    reasons: dict[str, int] = {}
    for f in s["failures"]:
        key = f"{f['kind']}:{f['reason']}"
        reasons[key] = reasons.get(key, 0) + 1
    print("failures:", reasons)


if __name__ == "__main__":
    main()
