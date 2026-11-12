"""Deterministic baseline extractor.

Regex and dictionary rules over buyer turns. It is the baseline any LLM extractor
has to beat on the eval: it costs nothing, runs in milliseconds, and its mistakes
are explainable. Confidence is fixed per rule: exact dictionary hits score higher
than phrase patterns, and a negation just before a match cuts confidence so the
signal drops out or goes to review instead of being written to the CRM.
"""

import re
from datetime import date

from .vocab import BUYER_SPEAKERS, SIGNAL_VOCAB

# (type, value, pattern, confidence). Patterns run on lowercased buyer turns.
RULES: list[tuple[str, str, str, float]] = [
    # Buying signals
    ("buying_signal", "requested_proposal", r"send (?:over )?(?:me )?(?:a |the )?(?:proposal|order form|contract)", 0.9),
    ("buying_signal", "asked_pricing", r"how does pricing work|send me pricing|what does it cost", 0.85),
    ("buying_signal", "intro_to_decision_maker", r"\b(?:cfo|ceo|cro|coo)\b[^.]*\b(?:see this|meet|join)\b", 0.75),
    ("buying_signal", "trial_request", r"\btrial\b|\bpilot\b", 0.8),
    # Objections
    ("objection", "price", r"expensive|the price|pricing would have to|cheaper", 0.75),
    ("objection", "timing", r"not looking to buy|not a priority|not this year", 0.8),
    ("objection", "authority", r"not the one who signs|not my decision|ask my boss", 0.85),
    ("objection", "security", r"soc ?2|security review|data residency|infosec", 0.8),
    ("objection", "need", r"(?:do not|don't) (?:think we )?need|no need for", 0.7),
    # Budget
    ("budget", "approved", r"budget (?:is|for [a-z ]+? is) (?:already )?approved|money is there", 0.85),
    ("budget", "constrained", r"budget freeze|money is tight|budget cut|got cut", 0.8),
    # Timing (quarter references are handled separately, relative to the call date)
    ("timing", "this_quarter", r"this quarter|end of quarter", 0.7),
    ("timing", "next_quarter", r"next quarter", 0.75),
    ("timing", "later", r"next year", 0.6),
    # Feature requests
    ("feature_request", "sso", r"\bsso\b|single sign-on", 0.9),
    ("feature_request", "salesforce_sync", r"salesforce sync|sync[a-z]* [^.]*salesforce", 0.75),
    ("feature_request", "api_access", r"\ban api\b|api access", 0.8),
    ("feature_request", "custom_reports", r"custom dashboards?|custom reports?|rollup", 0.75),
    ("feature_request", "commissions_integration", r"commission", 0.7),
    # Pain points
    ("pain_point", "manual_reporting", r"spreadsheets?|whiteboard|by hand|manually", 0.7),
    ("pain_point", "data_quality", r"duplicates|data is a mess|never match|bad data", 0.75),
    ("pain_point", "forecast_accuracy", r"forecast accuracy|missed (?:the |our )?(?:last|number)|forecast (?:is|was) (?:off|wrong)", 0.75),
    ("pain_point", "rep_ramp", r"\bramp\b", 0.75),
    # Churn risk (customer calls only, see POST_CALL_TYPES)
    ("churn_risk", "champion_left", r"\b(?:left|quit|departed)\b", 0.7),
    ("churn_risk", "low_usage", r"usage is low|logins dropped|went back to", 0.8),
    ("churn_risk", "budget_cut", r"budget freeze|budget cut|got cut", 0.75),
    # Expansion
    ("expansion_opportunity", "new_team", r"add the [a-z ]+ team|wants the same setup", 0.75),
    ("expansion_opportunity", "new_region", r"\b(?:canada|emea|europe|apac|latam)\b|new region", 0.75),
    ("expansion_opportunity", "upsell_tier", r"advanced [a-z ]+ package|upgrade to|premium tier", 0.75),
    # Content opportunities
    ("content_opportunity", "roi_case_study", r"case study|\broi\b", 0.7),
    ("content_opportunity", "security_doc", r"soc ?2|security questionnaire", 0.7),
    ("content_opportunity", "integration_guide", r"integration (?:docs|guide)", 0.85),
    ("content_opportunity", "adoption_guide", r"adoption guide|rollout plan", 0.7),
]

POST_CALL_TYPES = {"renewal", "qbr"}
CUSTOMER_ONLY = {"churn_risk", "expansion_opportunity"}
COMPETITOR_EVAL = r"quote from|evaluat|talking to|looking at"
NEGATION = re.compile(r"\b(?:not|never|no|ignore)\b")


def _negated(text: str, start: int) -> bool:
    window = text[max(0, start - 30):start]
    return bool(NEGATION.search(window))


def _quarter(d: date) -> int:
    return (d.month - 1) // 3 + 1


def _evidence(original: str, start: int, end: int) -> str:
    """Return the sentence of the original turn that contains the match."""
    left = max(original.rfind(".", 0, start), original.rfind("?", 0, start), original.rfind("!", 0, start))
    right_candidates = [i for i in (original.find(".", end), original.find("?", end), original.find("!", end)) if i != -1]
    right = min(right_candidates) + 1 if right_candidates else len(original)
    return original[left + 1:right].strip()


def extract(call: dict) -> list[dict]:
    signals: dict[tuple[str, str], dict] = {}
    call_date = date.fromisoformat(call["call_date"])
    post_call = call["call_type"] in POST_CALL_TYPES

    def add(sig_type: str, value: str, idx: int, text: str, start: int, end: int, conf: float) -> None:
        key = (sig_type, value)
        if key in signals and signals[key]["confidence"] >= conf:
            return
        signals[key] = {
            "type": sig_type,
            "value": value,
            "turn": idx,
            "evidence": _evidence(text, start, end),
            "confidence": conf,
            "extractor": "rules",
        }

    for idx, turn in enumerate(call["turns"]):
        if turn["speaker"] not in BUYER_SPEAKERS:
            continue
        original = turn["text"]
        text = original.lower()

        for sig_type, value, pattern, conf in RULES:
            if sig_type in CUSTOMER_ONLY and not post_call:
                continue
            m = re.search(pattern, text)
            if not m:
                continue
            if sig_type not in {"objection", "budget"} and _negated(text, m.start()):
                conf = round(conf - 0.4, 2)
            add(sig_type, value, idx, original, m.start(), m.end(), conf)

        for name in SIGNAL_VOCAB["competitor_mention"]:
            m = re.search(rf"\b{name.lower()}\b", text)
            if not m:
                continue
            add("competitor_mention", name, idx, original, m.start(), m.end(), 0.95)
            if post_call and re.search(COMPETITOR_EVAL, text) and not _negated(text, m.start()):
                add("churn_risk", "competitor_eval", idx, original, m.start(), m.end(), 0.8)

        m = re.search(r"\bq([1-4])\b", text)
        if m:
            delta = (int(m.group(1)) - _quarter(call_date)) % 4
            value = {0: "this_quarter", 1: "next_quarter"}.get(delta, "later")
            add("timing", value, idx, original, m.start(), m.end(), 0.7)

    return list(signals.values())
