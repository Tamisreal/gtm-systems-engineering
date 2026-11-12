"""Demo: python -m ontology   (from projects/gtm-ontology)"""

import json

from .build import build
from .graph import to_mermaid, triples
from .queries import account_360, committee_gaps, locations_within, renewals_at_risk, review_queue, whitespace


def main() -> None:
    conn = build()
    counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
              for t in ("source_record", "company", "location", "contact")}
    print("Loaded:", counts)
    print("\nMatch decisions:")
    for r in conn.execute("SELECT source_system, source_key, method, score, decision FROM match_decision"):
        print(f"  {r['source_system']:<10} {r['source_key']:<7} {r['method']:<9} {r['score']:<5} {r['decision']}")
    print("\nReview queue:", json.dumps(review_queue(conn), indent=2))
    print("\nAccount 360 (northgateins.com):", json.dumps(account_360(conn, "northgateins.com"), indent=2))
    print("\nWhitespace (riverbendcu.org):", whitespace(conn, "riverbendcu.org"))
    print("Committee gaps OPP-1:", committee_gaps(conn, "OPP-1"))
    print("Sites within 5 miles of downtown Houston:", locations_within(conn, 29.7604, -95.3698, 5))
    print("Renewals at risk:", renewals_at_risk(conn))
    cid = conn.execute("SELECT company_id FROM company WHERE domain = 'northgateins.com'").fetchone()[0]
    print("\nGraph view (Mermaid):\n" + to_mermaid(triples(conn, cid)))


if __name__ == "__main__":
    main()
