"""Unit tests for metric math plus the regression gate on the rules baseline.

Run from projects/ai-evaluation:  python -m unittest discover -s tests -t .
"""

import json
import unittest
from pathlib import Path

from evalkit.metrics import cost_usd, percentile, prf, score
from evalkit.run_eval import run

HERE = Path(__file__).resolve().parent.parent


class MetricMath(unittest.TestCase):
    def test_prf_basic(self):
        m = prf(tp=8, fp=2, fn=2)
        self.assertEqual((m["precision"], m["recall"], m["f1"]), (0.8, 0.8, 0.8))

    def test_prf_empty_is_zero_not_error(self):
        self.assertEqual(prf(0, 0, 0)["f1"], 0.0)

    def test_score_classifies_failures(self):
        truth = {"c1": [{"type": "objection", "value": "price"}, {"type": "timing", "value": "later"}]}
        preds = {"c1": [
            {"type": "objection", "value": "price", "evidence": "too expensive"},
            {"type": "timing", "value": "this_quarter", "evidence": "this quarter"},
            {"type": "churn_risk", "value": "competitor_eval", "evidence": "we ignore them"},
        ]}
        s = score(preds, truth)
        self.assertEqual(s["micro"]["tp"], 1)
        self.assertEqual(s["micro"]["fp"], 2)
        self.assertEqual(s["micro"]["fn"], 1)
        reasons = {(f["kind"], f["type"]): f["reason"] for f in s["failures"]}
        self.assertEqual(reasons[("false_positive", "timing")], "wrong_value")
        self.assertEqual(reasons[("false_positive", "churn_risk")], "negation_or_context")
        self.assertEqual(reasons[("false_negative", "timing")], "wrong_value")

    def test_cost(self):
        price = {"input_per_mtok": 4.0, "output_per_mtok": 20.0}
        self.assertAlmostEqual(cost_usd(1_000_000, 100_000, price), 6.0)

    def test_percentile(self):
        self.assertEqual(percentile([1, 2, 3, 4, 5], 0.5), 3)


class RegressionGate(unittest.TestCase):
    """Fails the build if the rules extractor drops below its recorded floor."""

    @classmethod
    def setUpClass(cls):
        cls.summary = run("rules", write=False)
        cls.gate = json.loads((HERE / "thresholds.json").read_text(encoding="utf-8"))["rules"]

    def test_micro_f1(self):
        self.assertGreaterEqual(self.summary["quality_kept"]["f1"], self.gate["micro_f1_min"])

    def test_auto_applied_precision(self):
        self.assertGreaterEqual(self.summary["quality_auto_applied"]["precision"],
                                self.gate["auto_applied_precision_min"])

    def test_every_signal_is_schema_valid_and_grounded(self):
        self.assertGreaterEqual(self.summary["structure"]["schema_and_grounding_valid_rate"],
                                self.gate["schema_and_grounding_valid_rate_min"])

    def test_review_load(self):
        self.assertLessEqual(self.summary["routing"]["review_share_of_kept"],
                             self.gate["review_share_of_kept_max"])


if __name__ == "__main__":
    unittest.main()
