"""From scores to an outreach queue a sequencer and a rep can act on.

Order of operations matters:
  1. Suppress first (do not contact, recently contacted). A suppressed account never gets a tier.
  2. Tier by score percentile within the eligible pool.
  3. Hold out a fixed share of Tier A and B from outreach. Without a holdout, any
     meetings that follow cannot be credited to the model: they might have come anyway.
  4. Assign a play per tier. Tier A goes to a person for review before anything is sent.
  5. Cap daily volume to what reps and mailboxes can carry.
"""

import hashlib

TIER_SHARES = (("A", 0.10), ("B", 0.20), ("C", 0.30))     # remaining 40%: no outreach
HOLDOUT_SHARE = 0.10

PLAYS = {
    "A": {"play": "AE-led, multithreaded, researched by hand", "channel": "email + call + LinkedIn", "review": "AE approves before send"},
    "B": {"play": "SDR sequence, first line from the strongest signal", "channel": "email + call", "review": "spot-check sample"},
    "C": {"play": "Low-touch nurture", "channel": "email", "review": "none"},
}

# Timely triggers first: a first line should say why now, not just why this company.
SIGNAL_PRIORITY = [
    ("new_revops_leader_90d", lambda a: a["new_revops_leader_90d"], "New RevOps leader in the last 90 days"),
    ("sales_roles_hiring_90d", lambda a: a["sales_roles_hiring_90d"] >= 3, "Hiring {n} sales roles in the last 90 days"),
    ("funded_12m", lambda a: a["funded_12m"], "Raised funding in the last 12 months"),
    ("uses_salesforce", lambda a: a["uses_salesforce"], "Runs Salesforce"),
]


def first_line_signal(a: dict) -> str | None:
    for _, present, text in SIGNAL_PRIORITY:
        if present(a):
            return text.format(n=a["sales_roles_hiring_90d"])
    return None


def in_holdout(account_id: str, share: float = HOLDOUT_SHARE) -> bool:
    """Deterministic: the same account is always in or out, across reruns."""
    h = int(hashlib.sha256(account_id.encode()).hexdigest()[:8], 16)
    return (h % 1000) < share * 1000


def suppression_reason(a: dict) -> str | None:
    if a.get("do_not_contact"):
        return "do_not_contact"
    if a.get("contacted_last_90d"):
        return "contacted_last_90d"
    return None


def build_queue(pool: list[dict], probs: list[float], reasons: list[list[tuple[str, float]]],
                daily_cap: int = 25) -> dict:
    suppressed, eligible = [], []
    for a, p, r in zip(pool, probs, reasons):
        why = suppression_reason(a)
        if why:
            suppressed.append({"account_id": a["account_id"], "reason": why})
        else:
            eligible.append((a, p, r))

    eligible.sort(key=lambda t: t[1], reverse=True)
    queue, holdout, untiered = [], [], 0
    start = 0
    bounds = []
    for tier, share in TIER_SHARES:
        end = start + round(len(eligible) * share)
        bounds.append((tier, start, end))
        start = end

    for idx, (a, p, r) in enumerate(eligible):
        tier = next((t for t, s, e in bounds if s <= idx < e), None)
        if tier is None:
            untiered += 1
            continue
        row = {
            "account_id": a["account_id"], "name": a["name"], "tier": tier,
            "win_probability": round(p, 3),
            "why": [n for n, _ in r],
            "first_line_signal": first_line_signal(a),
            **PLAYS[tier],
        }
        if tier in ("A", "B") and in_holdout(a["account_id"]):
            holdout.append({**row, "status": "holdout: no outreach, outcome tracked"})
            continue
        row["status"] = "pending_review" if tier == "A" else "ready"
        queue.append(row)

    for i, row in enumerate(queue):
        row["send_day"] = i // daily_cap + 1
    return {"queue": queue, "holdout": holdout, "suppressed": suppressed, "no_outreach": untiered}
