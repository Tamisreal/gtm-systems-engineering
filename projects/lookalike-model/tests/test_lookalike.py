"""Run from projects/lookalike-model:  python -m unittest discover -s tests -t ."""

import unittest

from lookalike.data import generate, split
from lookalike.evaluate import auc, calibration, lift_at, precision_at
from lookalike.features import POST_TOUCH_FIELDS, PRE_TOUCH_FIELDS, Standardizer, feature_names
from lookalike.outreach import build_queue, first_line_signal, in_holdout
from lookalike.pipeline import run


class Metrics(unittest.TestCase):
    def test_auc_perfect_random_and_ties(self):
        self.assertEqual(auc([0.9, 0.8, 0.2, 0.1], [1, 1, 0, 0]), 1.0)
        self.assertEqual(auc([0.1, 0.2, 0.8, 0.9], [1, 1, 0, 0]), 0.0)
        self.assertEqual(auc([0.5, 0.5], [1, 0]), 0.5)

    def test_precision_and_lift(self):
        scores, labels = [0.9, 0.8, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], [1, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(precision_at(scores, labels, 0.2), 0.5)
        self.assertAlmostEqual(lift_at(scores, labels, 0.2), 2.5)

    def test_calibration_bins_cover_everything(self):
        bins = calibration([i / 10 for i in range(10)], [0] * 5 + [1] * 5, bins=5)
        self.assertEqual(sum(b["n"] for b in bins), 10)


class DataDiscipline(unittest.TestCase):
    def test_generation_is_deterministic(self):
        self.assertEqual(generate()[:5], generate()[:5])

    def test_split_is_by_time_and_pool_is_untouched(self):
        train, test, pool = split(generate())
        self.assertLess(max(a["first_touch"] for a in train), min(a["first_touch"] for a in test))
        self.assertTrue(all(a["first_touch"] is None and a["meetings_held"] == 0 for a in pool))

    def test_no_post_touch_field_is_a_default_feature(self):
        self.assertFalse(PRE_TOUCH_FIELDS & POST_TOUCH_FIELDS)
        self.assertNotIn("meetings_held", feature_names())

    def test_standardizer_uses_training_statistics(self):
        s = Standardizer().fit([[0.0], [2.0]])
        self.assertEqual(s.transform([[4.0]]), [[3.0]])


class Outreach(unittest.TestCase):
    def pool(self):
        base = {"name": "x", "new_revops_leader_90d": False, "sales_roles_hiring_90d": 0,
                "funded_12m": False, "uses_salesforce": True}
        return [{**base, "account_id": f"P{i:03d}", "do_not_contact": i == 0, "contacted_last_90d": i == 1}
                for i in range(100)]

    def test_suppressed_accounts_never_get_a_tier(self):
        out = build_queue(self.pool(), [1 - i / 100 for i in range(100)], [[] for _ in range(100)])
        queued = {r["account_id"] for r in out["queue"] + out["holdout"]}
        self.assertNotIn("P000", queued)
        self.assertNotIn("P001", queued)
        self.assertEqual(len(out["suppressed"]), 2)

    def test_tier_a_waits_for_review(self):
        out = build_queue(self.pool(), [1 - i / 100 for i in range(100)], [[] for _ in range(100)])
        self.assertTrue(all(r["status"] == "pending_review" for r in out["queue"] if r["tier"] == "A"))

    def test_holdout_is_stable(self):
        self.assertEqual(in_holdout("A0001"), in_holdout("A0001"))

    def test_first_line_prefers_timely_trigger(self):
        a = {"new_revops_leader_90d": True, "sales_roles_hiring_90d": 5, "funded_12m": True, "uses_salesforce": True}
        self.assertEqual(first_line_signal(a), "New RevOps leader in the last 90 days")


class RegressionGate(unittest.TestCase):
    """The learned model must beat the written ICP, and the leakage trap must stay visible."""

    @classmethod
    def setUpClass(cls):
        cls.s = run(write=False)

    def test_model_beats_rule_baseline(self):
        m = self.s["models_on_test"]
        self.assertGreater(m["logistic_regression"]["auc"], m["rule_icp"]["auc"])

    def test_leaky_feature_looks_great_on_test(self):
        self.assertGreater(self.s["leakage_trap"]["test_auc_with_meetings_held"], 0.95)

    def test_leaky_model_cannot_rank_the_pool(self):
        t = self.s["leakage_trap"]
        self.assertLess(t["pool_score_spread_with_meetings_held"], t["pool_score_spread_without"])


if __name__ == "__main__":
    unittest.main()
