"""Normalization and identity resolution for company records.

Order of evidence, strongest first:
  1. normalized domain exact match            -> auto merge
  2. normalized phone (E.164) exact match     -> auto merge
  3. name similarity + physical proximity     -> auto merge only at high similarity, else review
  4. name similarity with no location to test -> review, never auto merge
  5. nothing                                  -> new entity

Probabilistic matches below the auto threshold go to a review queue instead of
merging. Two businesses in one strip mall with similar names are the classic
false merge, and a wrong merge is far more expensive to undo than a review.
"""

import math
import re
from difflib import SequenceMatcher
from urllib.parse import urlparse

SUFFIXES = {"inc", "llc", "ltd", "corp", "co", "company", "the", "group"}
ABBREVIATIONS = {"mfg": "manufacturing", "intl": "international", "svcs": "services"}

NAME_GEO_AUTO = 0.92        # similarity needed to auto merge when locations are close
NAME_REVIEW = 0.75          # similarity that is worth a person's time
NEAR_MILES = 0.25


def normalize_domain(raw: str | None) -> str | None:
    if not raw:
        return None
    raw = raw.strip().lower()
    host = urlparse(raw if "//" in raw else f"//{raw}").hostname or ""
    return host.removeprefix("www.") or None


def normalize_phone(raw: str | None) -> str | None:
    """US-only E.164. Returns None for anything that is not 10 or 11 (leading 1) digits."""
    if not raw:
        return None
    digits = re.sub(r"\D", "", raw)
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    return f"+1{digits}" if len(digits) == 10 else None


def normalize_name(raw: str) -> str:
    raw = raw.lower().split(" - ")[0]               # drop branch suffixes: "X - Katy Branch"
    tokens = re.sub(r"[^a-z0-9 ]", " ", raw).split()
    tokens = [ABBREVIATIONS.get(t, t) for t in tokens if t not in SUFFIXES]
    return " ".join(tokens)


def name_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, normalize_name(a), normalize_name(b)).ratio()


def miles_between(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 3958.8
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def match(record: dict, companies: list[dict], locations: list[dict]) -> dict:
    """Decide what a raw company record is.

    companies: [{"company_id", "canonical_name", "domain", "phones": set}]
    locations: [{"company_id", "name", "lat", "lon"}]
    Returns {"candidate_id", "method", "score", "decision"}.
    """
    domain = normalize_domain(record.get("domain"))
    phone = normalize_phone(record.get("phone"))

    for c in companies:
        if domain and c["domain"] == domain:
            return {"candidate_id": c["company_id"], "method": "domain", "score": 1.0, "decision": "auto_merge"}
    for c in companies:
        if phone and phone in c["phones"]:
            return {"candidate_id": c["company_id"], "method": "phone", "score": 0.95, "decision": "auto_merge"}

    best = {"candidate_id": None, "method": "none", "score": 0.0, "decision": "new_entity"}
    has_geo = record.get("lat") is not None and record.get("lon") is not None

    if has_geo:
        for loc in locations:
            if loc["lat"] is None:
                continue
            if miles_between(record["lat"], record["lon"], loc["lat"], loc["lon"]) > NEAR_MILES:
                continue
            sim = name_similarity(record["name"], loc["name"])
            if sim >= NAME_REVIEW and sim > best["score"]:
                decision = "auto_merge" if sim >= NAME_GEO_AUTO else "review"
                best = {"candidate_id": loc["company_id"], "method": "name_geo", "score": round(sim, 3), "decision": decision}
        return best

    for c in companies:
        sim = name_similarity(record["name"], c["canonical_name"])
        if sim >= NAME_REVIEW and sim > best["score"]:
            best = {"candidate_id": c["company_id"], "method": "name_only", "score": round(sim, 3), "decision": "review"}
    return best
