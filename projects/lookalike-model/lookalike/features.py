"""Feature encoding with an explicit allowlist.

Only fields known BEFORE first touch may be features. The allowlist is the leakage
control: a field is not used because it exists, it is used because someone decided
it is available at scoring time for an account nobody has contacted yet.
"""

import math

from .data import INDUSTRIES, REGIONS

PRE_TOUCH_FIELDS = {
    "industry", "region", "employees", "locations", "uses_salesforce",
    "sales_roles_hiring_90d", "funded_12m", "new_revops_leader_90d",
}
POST_TOUCH_FIELDS = {"meetings_held", "won", "first_touch"}


def _band(employees: int) -> str:
    if employees < 50:
        return "lt50"
    return "50_1000" if employees <= 1000 else "gt1000"


def feature_names(include_leaky: bool = False) -> list[str]:
    names = [f"industry={i}" for i in INDUSTRIES] + [f"region={r}" for r in REGIONS]
    names += ["emp_band=lt50", "emp_band=50_1000", "emp_band=gt1000",
              "log_locations", "uses_salesforce", "hiring_sales_roles", "funded_12m", "new_revops_leader_90d"]
    if include_leaky:
        names.append("meetings_held")
    return names


def encode(a: dict, include_leaky: bool = False) -> list[float]:
    x = [1.0 if a["industry"] == i else 0.0 for i in INDUSTRIES]
    x += [1.0 if a["region"] == r else 0.0 for r in REGIONS]
    band = _band(a["employees"])
    x += [1.0 if band == b else 0.0 for b in ("lt50", "50_1000", "gt1000")]
    x += [
        math.log(a["locations"]),
        float(a["uses_salesforce"]),
        min(a["sales_roles_hiring_90d"], 10) / 10,
        float(a["funded_12m"]),
        float(a["new_revops_leader_90d"]),
    ]
    if include_leaky:
        x.append(float(a["meetings_held"]))
    return x


class Standardizer:
    """Fit on training rows only, then apply to test and pool. Fitting on all rows leaks."""

    def fit(self, rows: list[list[float]]) -> "Standardizer":
        n, d = len(rows), len(rows[0])
        self.mean = [sum(r[j] for r in rows) / n for j in range(d)]
        self.std = [math.sqrt(sum((r[j] - self.mean[j]) ** 2 for r in rows) / n) or 1.0 for j in range(d)]
        return self

    def transform(self, rows: list[list[float]]) -> list[list[float]]:
        return [[(v - m) / s for v, m, s in zip(r, self.mean, self.std)] for r in rows]
