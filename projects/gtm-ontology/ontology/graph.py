"""Project the relational model into subject-predicate-object triples.

This is a graph VIEW of relational data, not a knowledge graph with an ontology
language, inference or a triple store. It is still useful: a graph is the natural
shape for "who at this account is connected to which deal" and for handing an
LLM a compact, typed context instead of raw tables.
"""

import sqlite3


def triples(conn: sqlite3.Connection, company_id: str) -> list[tuple[str, str, str]]:
    t: list[tuple[str, str, str]] = []
    co = conn.execute("SELECT canonical_name FROM company WHERE company_id = ?", (company_id,)).fetchone()
    name = co["canonical_name"]
    for r in conn.execute("SELECT name FROM location WHERE company_id = ?", (company_id,)):
        t.append((name, "HAS_LOCATION", r["name"]))
    for r in conn.execute("SELECT full_name FROM contact WHERE company_id = ?", (company_id,)):
        t.append((r["full_name"], "WORKS_AT", name))
    for r in conn.execute("SELECT o.name, p.name AS product FROM opportunity o JOIN account a USING (account_id) "
                          "LEFT JOIN product p USING (product_id) WHERE a.company_id = ?", (company_id,)):
        t.append((name, "HAS_OPPORTUNITY", r["name"]))
        if r["product"]:
            t.append((r["name"], "FOR_PRODUCT", r["product"]))
    for r in conn.execute("SELECT ct.full_name, b.role, o.name FROM buying_committee_member b "
                          "JOIN contact ct USING (contact_id) JOIN opportunity o USING (opportunity_id) "
                          "JOIN account a ON a.account_id = o.account_id WHERE a.company_id = ?", (company_id,)):
        t.append((r["full_name"], f"ROLE_{r['role'].upper()}", r["name"]))
    for r in conn.execute("SELECT p.name FROM contract ct JOIN customer cu USING (customer_id) "
                          "JOIN account a USING (account_id) JOIN product p USING (product_id) WHERE a.company_id = ?",
                          (company_id,)):
        t.append((name, "HAS_CONTRACT_FOR", r["name"]))
    for r in conn.execute("SELECT type, value FROM intent_signal WHERE company_id = ?", (company_id,)):
        t.append((name, f"SIGNAL_{r['type'].upper()}", r["value"]))
    return t


def to_mermaid(edges: list[tuple[str, str, str]]) -> str:
    ids: dict[str, str] = {}

    def node(label: str) -> str:
        if label not in ids:
            ids[label] = f"n{len(ids)}"
        return ids[label]

    lines = ["flowchart LR"]
    body = [f'    {node(s)} -- "{p}" --> {node(o)}' for s, p, o in edges]
    lines += [f'    {i}["{label}"]' for label, i in ids.items()]
    return "\n".join(lines + body)
