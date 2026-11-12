"""End to end: transcript -> extraction -> validation -> routing -> CRM operations.

Usage (from projects/conversation-intelligence):
    python -m ci.pipeline                 # rules extractor, all calls, summary
    python -m ci.pipeline --call call_005 # one call, full detail
    python -m ci.pipeline --extractor llm # Claude extractor (needs anthropic + credentials)
"""

import argparse
import json
from pathlib import Path

from . import llm, rules
from .crm import to_operations
from .route import route_all
from .validate import split_valid

DATA = Path(__file__).resolve().parent.parent / "data" / "transcripts.json"


def load_calls(path: Path = DATA) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["calls"]


def process(call: dict, extractor: str = "rules") -> dict:
    if extractor == "llm":
        raw, telemetry = llm.extract(call)
    else:
        raw, telemetry = rules.extract(call), {}
    valid, rejected = split_valid(raw, call)
    routed = route_all(valid)
    return {
        "call_id": call["call_id"],
        "account": call["account"],
        "raw": raw,
        "rejected": rejected,
        "routed": routed,
        "crm_operations": to_operations(call, routed["auto"]),
        "telemetry": telemetry,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--call")
    parser.add_argument("--extractor", choices=["rules", "llm"], default="rules")
    args = parser.parse_args()

    calls = load_calls()
    if args.call:
        calls = [c for c in calls if c["call_id"] == args.call]
    if args.extractor == "llm" and not llm.available():
        raise SystemExit("Install the anthropic package and set credentials to use --extractor llm.")

    for call in calls:
        result = process(call, args.extractor)
        r = result["routed"]
        print(f"{result['call_id']} {result['account']}: "
              f"{len(r['auto'])} auto, {len(r['review'])} review, {len(r['drop'])} dropped, "
              f"{len(result['rejected'])} rejected")
        if args.call:
            print(json.dumps({k: result[k] for k in ("routed", "rejected", "crm_operations")}, indent=2))


if __name__ == "__main__":
    main()
