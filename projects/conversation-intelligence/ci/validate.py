"""Boundary validation for extracted signals.

Two checks run on every signal, whichever extractor produced it:

1. Schema: required fields, types, and (type, value) membership in the vocabulary.
2. Grounding: the evidence quote must appear verbatim in the cited turn, and that
   turn must belong to the buyer. A model can return schema-valid JSON that quotes
   something nobody said; this check is what catches it.
"""

from .vocab import BUYER_SPEAKERS, SIGNAL_VOCAB

REQUIRED = {"type": str, "value": str, "evidence": str, "turn": int, "confidence": (int, float)}


def _norm(text: str) -> str:
    return " ".join(text.lower().split())


def validate_signal(signal: dict, call: dict) -> list[str]:
    """Return a list of error codes. Empty list means the signal is valid."""
    errors: list[str] = []
    for field, kind in REQUIRED.items():
        if field not in signal:
            errors.append(f"missing_field:{field}")
        elif not isinstance(signal[field], kind) or isinstance(signal[field], bool):
            errors.append(f"wrong_type:{field}")
    if errors:
        return errors

    if signal["type"] not in SIGNAL_VOCAB:
        errors.append("unknown_type")
    elif signal["value"] not in SIGNAL_VOCAB[signal["type"]]:
        errors.append("value_not_in_vocab")

    if not 0.0 <= float(signal["confidence"]) <= 1.0:
        errors.append("confidence_out_of_range")

    turns = call["turns"]
    if not 0 <= signal["turn"] < len(turns):
        errors.append("turn_out_of_range")
        return errors

    turn = turns[signal["turn"]]
    if turn["speaker"] not in BUYER_SPEAKERS:
        errors.append("evidence_from_seller")
    if not signal["evidence"].strip() or _norm(signal["evidence"]) not in _norm(turn["text"]):
        errors.append("evidence_not_in_turn")
    return errors


def split_valid(signals: list[dict], call: dict) -> tuple[list[dict], list[dict]]:
    """Partition signals into (valid, rejected). Rejected signals carry their errors."""
    valid, rejected = [], []
    for s in signals:
        errs = validate_signal(s, call)
        if errs:
            rejected.append({**s, "errors": errs})
        else:
            valid.append(s)
    return valid, rejected
