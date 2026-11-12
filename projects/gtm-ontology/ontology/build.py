"""Load raw source records into the canonical model with lineage and match decisions.

Source priority is the CRM first, because it is the system of record for the
relationship. Field survivorship is explicit, one owner per field:
  canonical_name          CRM, else first source seen
  industry, employee_band enrichment
  lat, lon, category      places
A later source can fill a NULL field it owns; it never overwrites a field another
source owns. That rule is what keeps three systems from fighting over one value.
"""

import json
import sqlite3
from pathlib import Path

from .resolve import match, normalize_domain, normalize_phone

HERE = Path(__file__).resolve().parent.parent
SOURCE_ORDER = {"crm": 0, "enrichment": 1, "places": 2}


def connect(path: str = ":memory:") -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript((HERE / "schema.sql").read_text(encoding="utf-8"))
    return conn


def _record_lineage(conn, rec: dict, entity_type: str, entity_id: str | None) -> None:
    conn.execute("INSERT INTO source_record VALUES (?, ?, ?, ?, ?)",
                 (rec["source"], rec["key"], entity_type, entity_id, json.dumps(rec, sort_keys=True)))


def load_companies(conn, records: list[dict]) -> None:
    companies: list[dict] = []
    locations: list[dict] = []
    n_company = n_location = 0

    for rec in sorted(records, key=lambda r: SOURCE_ORDER[r["source"]]):
        m = match(rec, companies, locations)
        conn.execute("INSERT INTO match_decision VALUES (?, ?, ?, ?, ?, ?)",
                     (rec["source"], rec["key"], m["candidate_id"], m["method"], m["score"], m["decision"]))

        if m["decision"] == "review":
            _record_lineage(conn, rec, "company", None)      # parked until a person decides
            continue

        if m["decision"] == "new_entity":
            n_company += 1
            company_id = f"CO-{n_company:03d}"
            conn.execute("INSERT INTO company (company_id, canonical_name, domain) VALUES (?, ?, ?)",
                         (company_id, rec["name"], normalize_domain(rec.get("domain"))))
            companies.append({"company_id": company_id, "canonical_name": rec["name"],
                              "domain": normalize_domain(rec.get("domain")), "phones": set()})
        else:
            company_id = m["candidate_id"]

        company = next(c for c in companies if c["company_id"] == company_id)
        if phone := normalize_phone(rec.get("phone")):
            company["phones"].add(phone)
        if not company["domain"] and (domain := normalize_domain(rec.get("domain"))):
            company["domain"] = domain
            conn.execute("UPDATE company SET domain = ? WHERE company_id = ?", (domain, company_id))

        if rec["source"] == "enrichment":
            conn.execute("UPDATE company SET industry = COALESCE(industry, ?), employee_band = COALESCE(employee_band, ?) "
                         "WHERE company_id = ?", (rec.get("industry"), rec.get("employee_band"), company_id))

        # A CRM or places record with an address is a physical site. Places adds coordinates.
        if rec.get("address"):
            existing = next((l for l in locations if l["company_id"] == company_id and l["address"] == rec["address"]), None)
            if existing is None:
                n_location += 1
                existing = {"location_id": f"LOC-{n_location:03d}", "company_id": company_id, "name": rec["name"],
                            "address": rec["address"], "lat": None, "lon": None}
                locations.append(existing)
                conn.execute("INSERT INTO location (location_id, company_id, name, address, phone_e164) VALUES (?, ?, ?, ?, ?)",
                             (existing["location_id"], company_id, rec["name"], rec["address"], normalize_phone(rec.get("phone"))))
            if rec["source"] == "places":
                existing.update(lat=rec["lat"], lon=rec["lon"], name=rec["name"])
                conn.execute("UPDATE location SET lat = ?, lon = ?, category = ?, name = ? WHERE location_id = ?",
                             (rec["lat"], rec["lon"], rec.get("category"), rec["name"], existing["location_id"]))

        _record_lineage(conn, rec, "company", company_id)


def _company_id(conn, domain: str) -> str:
    return conn.execute("SELECT company_id FROM company WHERE domain = ?", (domain,)).fetchone()["company_id"]


def load_contacts(conn, records: list[dict]) -> None:
    """Contacts resolve on lowercased email. The CRM title wins; enrichment fills gaps."""
    seen: dict[str, str] = {}
    for rec in sorted(records, key=lambda r: SOURCE_ORDER[r["source"]]):
        email = rec["email"].strip().lower()
        if email not in seen:
            contact_id = f"CT-{len(seen) + 1:03d}"
            seen[email] = contact_id
            conn.execute("INSERT INTO contact VALUES (?, ?, ?, ?, ?)",
                         (contact_id, _company_id(conn, rec["domain"]), rec["full_name"], rec["title"], email))
        _record_lineage(conn, rec, "contact", seen[email])


def load_commercial(conn, data: dict) -> None:
    for i, a in enumerate(data["accounts"], 1):
        conn.execute("INSERT INTO account VALUES (?, ?, ?, ?, ?)",
                     (f"AC-{i:03d}", _company_id(conn, a["domain"]), a["owner"], a["tier"], a["status"]))
    for p in data["products"]:
        conn.execute("INSERT INTO product VALUES (?, ?, ?)", (p["product_id"], p["name"], p["family"]))
    for s in data["services"]:
        conn.execute("INSERT INTO service VALUES (?, ?)", (s["service_id"], s["name"]))

    def account_id(domain: str) -> str:
        return conn.execute("SELECT a.account_id FROM account a JOIN company c USING (company_id) WHERE c.domain = ?",
                            (domain,)).fetchone()["account_id"]

    def contact_id(email: str) -> str:
        return conn.execute("SELECT contact_id FROM contact WHERE email = ?", (email,)).fetchone()["contact_id"]

    for i, c in enumerate(data["contracts"], 1):
        acc = account_id(c["domain"])
        cust = conn.execute("SELECT customer_id FROM customer WHERE account_id = ?", (acc,)).fetchone()
        if cust is None:
            cust_id = f"CU-{acc[3:]}"
            conn.execute("INSERT INTO customer VALUES (?, ?, ?)", (cust_id, acc, c["start"]))
        else:
            cust_id = cust["customer_id"]
        conn.execute("INSERT INTO contract VALUES (?, ?, ?, ?, ?, ?)",
                     (f"CN-{i:03d}", cust_id, c["product_id"], c["start"], c["end"], c["arr"]))

    for o in data["opportunities"]:
        conn.execute("INSERT INTO opportunity VALUES (?, ?, ?, ?, ?, ?, ?)",
                     (o["opportunity_id"], account_id(o["domain"]), o["product_id"], o["name"], o["stage"], o["amount"], o["close_date"]))
        for m in o["committee"]:
            conn.execute("INSERT INTO buying_committee_member VALUES (?, ?, ?)",
                         (o["opportunity_id"], contact_id(m["email"]), m["role"]))

    for s in data["intent_signals"]:
        conn.execute("INSERT INTO intent_signal (company_id, type, value, observed_at, source, confidence) VALUES (?, ?, ?, ?, ?, ?)",
                     (_company_id(conn, s["domain"]), s["type"], s["value"], s["observed_at"], s["source"], s["confidence"]))
    for a in data["activities"]:
        conn.execute("INSERT INTO activity (account_id, contact_id, type, occurred_at, summary) VALUES (?, ?, ?, ?, ?)",
                     (account_id(a["domain"]), contact_id(a["email"]), a["type"], a["occurred_at"], a["summary"]))


def build(path: str = ":memory:") -> sqlite3.Connection:
    data = json.loads((HERE / "data" / "source_records.json").read_text(encoding="utf-8"))
    conn = connect(path)
    load_companies(conn, data["company_records"])
    load_contacts(conn, data["contacts"])
    load_commercial(conn, data["commercial"])
    conn.commit()
    return conn
