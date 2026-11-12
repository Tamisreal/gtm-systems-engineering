"""Questions the model answers, plus a small semantic layer.

The semantic layer is the point where a metric gets ONE definition. "ARR" written
three ways in three dashboards is how a board deck and a CRM report disagree.
Here every consumer (a dashboard, an AI assistant answering "what is Northgate's
ARR?") calls the same function backed by the same SQL.
"""

import sqlite3

from .resolve import miles_between

AS_OF = "2026-11-12"

SEMANTIC_METRICS = {
    "active_arr": {
        "definition": "Sum of contract ARR where the contract covers the as-of date.",
        "sql": "SELECT COALESCE(SUM(ct.arr), 0) FROM contract ct JOIN customer cu USING (customer_id) "
               "JOIN account a USING (account_id) WHERE a.company_id = :company_id "
               "AND ct.start_date <= :as_of AND ct.end_date >= :as_of",
    },
    "open_pipeline": {
        "definition": "Sum of opportunity amount for opportunities not in a closed stage.",
        "sql": "SELECT COALESCE(SUM(o.amount), 0) FROM opportunity o JOIN account a USING (account_id) "
               "WHERE a.company_id = :company_id AND o.stage NOT IN ('Closed Won', 'Closed Lost')",
    },
    "location_count": {
        "definition": "Physical sites resolved to the company.",
        "sql": "SELECT COUNT(*) FROM location WHERE company_id = :company_id",
    },
}

REQUIRED_ROLES = ("economic_buyer", "champion", "technical_evaluator")


def metric(conn: sqlite3.Connection, name: str, company_id: str, as_of: str = AS_OF) -> float:
    row = conn.execute(SEMANTIC_METRICS[name]["sql"], {"company_id": company_id, "as_of": as_of}).fetchone()
    return row[0]


def company_by_domain(conn, domain: str) -> sqlite3.Row:
    return conn.execute("SELECT * FROM company WHERE domain = ?", (domain,)).fetchone()


def account_360(conn, domain: str, as_of: str = AS_OF) -> dict:
    """Everything an AE, AM or an AI assistant needs about one account, with sources."""
    co = company_by_domain(conn, domain)
    cid = co["company_id"]
    rows = lambda sql: [dict(r) for r in conn.execute(sql, (cid,))]  # noqa: E731
    return {
        "company": dict(co),
        "account": rows("SELECT owner, tier, status FROM account WHERE company_id = ?"),
        "locations": rows("SELECT name, address, lat, lon FROM location WHERE company_id = ?"),
        "contacts": rows("SELECT full_name, title, email FROM contact WHERE company_id = ?"),
        "open_opportunities": rows(
            "SELECT o.opportunity_id, o.name, o.stage, o.amount FROM opportunity o "
            "JOIN account a USING (account_id) WHERE a.company_id = ? AND o.stage NOT IN ('Closed Won', 'Closed Lost')"),
        "signals": rows("SELECT type, value, observed_at, source, confidence FROM intent_signal WHERE company_id = ? "
                        "ORDER BY observed_at DESC"),
        "metrics": {name: metric(conn, name, cid, as_of) for name in SEMANTIC_METRICS},
        "sources": rows("SELECT source_system, source_key FROM source_record WHERE entity_id = ?"),
    }


def locations_within(conn, lat: float, lon: float, radius_miles: float) -> list[dict]:
    """Territory question: every resolved site inside a radius, nearest first."""
    out = []
    for r in conn.execute("SELECT l.*, c.canonical_name FROM location l JOIN company c USING (company_id) "
                          "WHERE l.lat IS NOT NULL"):
        d = miles_between(lat, lon, r["lat"], r["lon"])
        if d <= radius_miles:
            out.append({"company": r["canonical_name"], "site": r["name"], "miles": round(d, 2)})
    return sorted(out, key=lambda x: x["miles"])


def whitespace(conn, domain: str, as_of: str = AS_OF) -> list[str]:
    """Products the company has no active contract or open opportunity for."""
    cid = company_by_domain(conn, domain)["company_id"]
    rows = conn.execute(
        "SELECT p.name FROM product p WHERE p.product_id NOT IN ("
        "  SELECT ct.product_id FROM contract ct JOIN customer cu USING (customer_id) JOIN account a USING (account_id)"
        "  WHERE a.company_id = :cid AND ct.end_date >= :as_of"
        "  UNION SELECT o.product_id FROM opportunity o JOIN account a USING (account_id)"
        "  WHERE a.company_id = :cid AND o.stage NOT IN ('Closed Won', 'Closed Lost')) ORDER BY p.name",
        {"cid": cid, "as_of": as_of})
    return [r["name"] for r in rows]


def committee_gaps(conn, opportunity_id: str) -> list[str]:
    """Required buying-committee roles with nobody mapped to them."""
    filled = {r["role"] for r in conn.execute(
        "SELECT role FROM buying_committee_member WHERE opportunity_id = ?", (opportunity_id,))}
    return [r for r in REQUIRED_ROLES if r not in filled]


def review_queue(conn) -> list[dict]:
    return [dict(r) for r in conn.execute(
        "SELECT m.source_system, m.source_key, json_extract(s.payload_json, '$.name') AS record_name, "
        "c.canonical_name AS candidate, m.method, m.score FROM match_decision m "
        "JOIN source_record s USING (source_system, source_key) "
        "LEFT JOIN company c ON c.company_id = m.candidate_id WHERE m.decision = 'review'")]


def renewals_at_risk(conn, as_of: str = AS_OF, window_days: int = 120) -> list[dict]:
    """Contracts ending soon on accounts with a churn signal: the CSM's worklist."""
    return [dict(r) for r in conn.execute(
        "SELECT c.canonical_name, ct.end_date, ct.arr, GROUP_CONCAT(DISTINCT s.value) AS churn_signals "
        "FROM contract ct JOIN customer cu USING (customer_id) JOIN account a USING (account_id) "
        "JOIN company c USING (company_id) JOIN intent_signal s ON s.company_id = c.company_id AND s.type = 'churn_risk' "
        "WHERE julianday(ct.end_date) - julianday(:as_of) <= :w GROUP BY ct.contract_id ORDER BY ct.end_date",
        {"as_of": as_of, "w": window_days})]
