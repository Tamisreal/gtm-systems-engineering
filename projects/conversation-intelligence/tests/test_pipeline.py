"""Behavior tests for validation, extraction edge cases, routing and CRM operations.

Run from projects/conversation-intelligence:  python -m unittest discover -s tests -t .
"""

import unittest

from ci import rules
from ci.crm import idempotency_key, to_operations
from ci.pipeline import load_calls, process
from ci.route import route
from ci.validate import validate_signal

CALL = {
    "call_id": "t1", "account": "Test Co", "call_type": "discovery", "call_date": "2026-05-14",
    "turns": [
        {"speaker": "rep", "text": "Is price a concern?"},
        {"speaker": "prospect", "text": "Budget is approved for Q3. We are not talking to PipeGrid."},
    ],
}


def sig(**overrides):
    base = {"type": "budget", "value": "approved", "turn": 1,
            "evidence": "Budget is approved for Q3.", "confidence": 0.9}
    return {**base, **overrides}


class Validation(unittest.TestCase):
    def test_valid_signal_passes(self):
        self.assertEqual(validate_signal(sig(), CALL), [])

    def test_hallucinated_quote_is_rejected(self):
        errs = validate_signal(sig(evidence="We signed the contract yesterday."), CALL)
        self.assertIn("evidence_not_in_turn", errs)

    def test_quote_from_seller_is_rejected(self):
        errs = validate_signal(sig(type="objection", value="price", turn=0, evidence="Is price a concern?"), CALL)
        self.assertIn("evidence_from_seller", errs)

    def test_value_outside_vocabulary_is_rejected(self):
        self.assertIn("value_not_in_vocab", validate_signal(sig(value="maybe"), CALL))

    def test_missing_field_is_rejected(self):
        bad = sig()
        del bad["confidence"]
        self.assertIn("missing_field:confidence", validate_signal(bad, CALL))


class Extraction(unittest.TestCase):
    def test_quarter_is_resolved_relative_to_call_date(self):
        found = {(s["type"], s["value"]) for s in rules.extract(CALL)}
        self.assertIn(("timing", "next_quarter"), found)

    def test_negated_competitor_is_not_a_churn_signal(self):
        found = {(s["type"], s["value"]) for s in rules.extract({**CALL, "call_type": "renewal"})}
        self.assertIn(("competitor_mention", "PipeGrid"), found)
        self.assertNotIn(("churn_risk", "competitor_eval"), found)

    def test_churn_rules_skip_prospect_calls(self):
        call = {**CALL, "turns": [{"speaker": "prospect", "text": "Our VP left last month."}]}
        self.assertFalse([s for s in rules.extract(call) if s["type"] == "churn_risk"])

    def test_every_extracted_signal_validates_on_the_dataset(self):
        for call in load_calls():
            result = process(call)
            self.assertEqual(result["rejected"], [], call["call_id"])


class RoutingAndCrm(unittest.TestCase):
    def test_high_impact_always_reviewed(self):
        self.assertEqual(route(sig(type="churn_risk", value="low_usage", confidence=0.99)), "review")

    def test_bands(self):
        self.assertEqual(route(sig(confidence=0.85)), "auto")
        self.assertEqual(route(sig(confidence=0.6)), "review")
        self.assertEqual(route(sig(confidence=0.3)), "drop")

    def test_idempotency_key_is_stable(self):
        self.assertEqual(idempotency_key("t1", sig()), idempotency_key("t1", sig(confidence=0.5)))
        self.assertNotEqual(idempotency_key("t1", sig()), idempotency_key("t2", sig()))

    def test_operations_carry_evidence(self):
        op = to_operations(CALL, [sig()])[0]
        self.assertEqual((op["object"], op["target"]), ("Opportunity", "Budget_Status__c"))
        self.assertEqual(op["evidence"], "Budget is approved for Q3.")


if __name__ == "__main__":
    unittest.main()
