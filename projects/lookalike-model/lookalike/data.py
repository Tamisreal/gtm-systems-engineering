"""Deterministic synthetic account universe.

1,000 invented accounts. 700 were worked by sales between 2025-07-01 and 2026-09-30
and have an outcome (closed won or not). 300 have never been contacted: that is
the prospect pool the model scores for outreach.

Outcomes come from a hidden propensity function plus noise, so a model has a real
pattern to find and cannot find it perfectly. Because the same code defines the
pattern and the model, scores here are optimistic by construction.

`meetings_held` is a deliberate leakage trap: it is recorded AFTER first touch,
it is strongly related to winning, and it is zero for every account in the pool.
"""

import math
import random
from datetime import date, timedelta

INDUSTRIES = ["software", "fintech", "healthcare", "logistics", "manufacturing", "retail", "education", "insurance"]
REGIONS = ["northeast", "south", "midwest", "west"]
CORE_INDUSTRIES = {"logistics", "manufacturing", "insurance"}   # hidden truth, not given to the model

TOUCH_START = date(2025, 7, 1)
TOUCH_DAYS = 456                                                 # through 2026-09-30
SPLIT_DATE = date(2026, 4, 1)                                    # train before, test on or after


def _sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))


def generate(seed: int = 7, n: int = 1000, n_touched: int = 700) -> list[dict]:
    rng = random.Random(seed)
    accounts = []
    for i in range(n):
        employees = max(5, min(20000, int(math.exp(rng.gauss(5.0, 1.2)))))
        industry = rng.choice(INDUSTRIES)
        a = {
            "account_id": f"A{i:04d}",
            "name": f"Synthetic Account {i:04d}",
            "industry": industry,
            "region": rng.choice(REGIONS),
            "employees": employees,
            "locations": 1 + int(rng.expovariate(1 / 2)),
            "uses_salesforce": rng.random() < (0.35 + 0.25 * (employees > 200)),
            "sales_roles_hiring_90d": min(25, int(rng.expovariate(1 / 3))),
            "funded_12m": rng.random() < 0.2,
            "new_revops_leader_90d": rng.random() < 0.15,
        }
        logit = (-3.4
                 + 1.3 * (industry in CORE_INDUSTRIES)
                 + 1.0 * (50 <= employees <= 1000)
                 + 0.6 * a["uses_salesforce"]
                 + 0.12 * min(a["sales_roles_hiring_90d"], 10)
                 + 0.9 * a["new_revops_leader_90d"]
                 + 0.4 * a["funded_12m"]
                 + rng.gauss(0, 0.6))
        if i < n_touched:
            a["first_touch"] = (TOUCH_START + timedelta(days=rng.randrange(TOUCH_DAYS))).isoformat()
            a["won"] = rng.random() < _sigmoid(logit)
            a["meetings_held"] = (2 + rng.randint(0, 3)) if a["won"] else (1 if rng.random() < 0.25 else 0)
        else:
            a["first_touch"] = None
            a["won"] = None
            a["meetings_held"] = 0
            a["do_not_contact"] = rng.random() < 0.03
            a["contacted_last_90d"] = rng.random() < 0.08
        accounts.append(a)
    return accounts


def split(accounts: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    """Time-based split: (train, test, pool). Never a random split on time-ordered outcomes."""
    touched = [a for a in accounts if a["first_touch"]]
    train = [a for a in touched if date.fromisoformat(a["first_touch"]) < SPLIT_DATE]
    test = [a for a in touched if date.fromisoformat(a["first_touch"]) >= SPLIT_DATE]
    pool = [a for a in accounts if not a["first_touch"]]
    return train, test, pool
