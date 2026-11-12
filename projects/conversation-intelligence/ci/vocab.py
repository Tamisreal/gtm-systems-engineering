"""Controlled vocabulary for call signals.

Every extracted signal is a (type, value) pair from this table. A closed vocabulary
is what makes the output usable downstream: a CRM picklist, a routing rule and an
eval can all key on "objection/price", while free text cannot be counted.
"""

SIGNAL_VOCAB: dict[str, list[str]] = {
    "buying_signal": ["requested_proposal", "asked_pricing", "intro_to_decision_maker", "trial_request"],
    "objection": ["price", "timing", "authority", "integration", "security", "need"],
    "competitor_mention": ["PipeGrid", "Forecastly", "SignalStack"],
    "budget": ["approved", "constrained"],
    "timing": ["this_quarter", "next_quarter", "later"],
    "feature_request": ["sso", "salesforce_sync", "api_access", "custom_reports", "commissions_integration"],
    "pain_point": ["manual_reporting", "data_quality", "forecast_accuracy", "rep_ramp"],
    "churn_risk": ["champion_left", "low_usage", "competitor_eval", "budget_cut"],
    "expansion_opportunity": ["new_team", "new_region", "upsell_tier"],
    "content_opportunity": ["roi_case_study", "security_doc", "integration_guide", "adoption_guide"],
}

SIGNAL_TYPES = list(SIGNAL_VOCAB)

# Signals that change an account's commercial status. These always go to a person,
# whatever the confidence, because a wrong "churn risk" flag triggers a save play
# and a wrong expansion flag sends an AM after a customer who is not ready.
HIGH_IMPACT_TYPES = {"churn_risk", "expansion_opportunity"}

BUYER_SPEAKERS = {"prospect", "customer"}
