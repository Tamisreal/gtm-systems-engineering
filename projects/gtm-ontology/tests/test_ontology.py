"""Run from projects/gtm-ontology:  python -m unittest discover -s tests -t ."""

import unittest

from ontology.build import build
from ontology.graph import triples
from ontology.queries import account_360, committee_gaps, locations_within, metric, review_queue, whitespace
from ontology.resolve import name_similarity, normalize_domain, normalize_name, normalize_phone


class Normalization(unittest.TestCase):
    def test_domain(self):
        self.assertEqual(normalize_domain("https://www.NorthgateIns.com/about"), "northgateins.com")
        self.assertEqual(normalize_domain("www.riverbendcu.org"), "riverbendcu.org")
        self.assertIsNone(normalize_domain(""))

    def test_phone(self):
        for raw in ("(713) 555-0142", "713.555.0142", "+1 713 555 0142"):
            self.assertEqual(normalize_phone(raw), "+17135550142")
        self.assertIsNone(normalize_phone("555-0142"))

    def test_name(self):
        self.assertEqual(normalize_name("Summit Dental Group, LLC"), "summit dental")
        self.assertEqual(normalize_name("Riverbend Credit Union - Katy Branch"), "riverbend credit union")
        self.assertGreater(name_similarity("Copper Line Mfg", "Copperline Manufacturing"), 0.9)


class Resolution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = build()

    def decision(self, key):
        return self.conn.execute("SELECT method, decision FROM match_decision WHERE source_key = ?", (key,)).fetchone()

    def test_domain_variant_merges(self):
        self.assertEqual(tuple(self.decision("enr-77")), ("domain", "auto_merge"))

    def test_phone_merges_across_different_domains(self):
        self.assertEqual(tuple(self.decision("enr-78")), ("phone", "auto_merge"))

    def test_branches_become_locations_not_companies(self):
        co = self.conn.execute("SELECT company_id FROM company WHERE domain = 'riverbendcu.org'").fetchone()[0]
        self.assertEqual(metric(self.conn, "location_count", co), 2)
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM company WHERE canonical_name LIKE 'Riverbend%'").fetchone()[0], 1)

    def test_strip_mall_neighbor_is_reviewed_not_merged(self):
        self.assertEqual(tuple(self.decision("pl-305")), ("name_geo", "review"))

    def test_name_only_match_is_never_auto_merged(self):
        self.assertEqual(tuple(self.decision("enr-79")), ("name_only", "review"))
        self.assertEqual(len(review_queue(self.conn)), 2)

    def test_survivorship_crm_name_enrichment_firmographics(self):
        c = account_360(self.conn, "northgateins.com")["company"]
        self.assertEqual((c["canonical_name"], c["industry"]), ("Northgate Insurance Inc.", "Insurance"))

    def test_contacts_dedupe_on_email_case(self):
        n = self.conn.execute("SELECT COUNT(*) FROM contact WHERE email = 'maya.chen@northgateins.com'").fetchone()[0]
        self.assertEqual(n, 1)

    def test_lineage_covers_every_source_record(self):
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM source_record").fetchone()[0], 19)
        sources = {r["source_system"] for r in account_360(self.conn, "northgateins.com")["sources"]}
        self.assertEqual(sources, {"crm", "enrichment", "places"})


class Questions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = build()

    def test_semantic_metrics(self):
        m = account_360(self.conn, "northgateins.com")["metrics"]
        self.assertEqual((m["active_arr"], m["open_pipeline"]), (48000, 36000))

    def test_whitespace_excludes_owned_and_in_flight(self):
        self.assertEqual(whitespace(self.conn, "northgateins.com"), ["Data API"])

    def test_committee_gaps(self):
        self.assertEqual(committee_gaps(self.conn, "OPP-2"), ["economic_buyer", "champion", "technical_evaluator"])

    def test_radius_query(self):
        names = [r["site"] for r in locations_within(self.conn, 29.7604, -95.3698, 2)]
        self.assertEqual(names, ["Northgate Insurance", "Riverbend Credit Union - Westheimer Branch"])

    def test_graph_view(self):
        co = self.conn.execute("SELECT company_id FROM company WHERE domain = 'northgateins.com'").fetchone()[0]
        self.assertIn(("Maya Chen", "ROLE_CHAMPION", "Northgate Canada expansion"), triples(self.conn, co))


if __name__ == "__main__":
    unittest.main()
