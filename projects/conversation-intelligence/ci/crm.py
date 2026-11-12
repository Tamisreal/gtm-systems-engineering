"""Turn auto-approved signals into idempotent CRM operations.

The output is a list of operations a CRM adapter would apply (Salesforce, HubSpot,
or anything with upsert-by-external-id). Nothing here calls a CRM. Each operation
carries an idempotency key built from (call, type, value), so re-processing the same
call after a retry produces the same keys and the adapter can skip duplicates.
"""

import hashlib

# Where each signal type lands. Field names are illustrative, not a real org's schema.
FIELD_MAP = {
    "competitor_mention": ("Opportunity", "add_to_multiselect", "Competitors__c"),
    "objection": ("Opportunity", "add_to_multiselect", "Open_Objections__c"),
    "budget": ("Opportunity", "set_field", "Budget_Status__c"),
    "timing": ("Opportunity", "set_field", "Buyer_Timeline__c"),
    "pain_point": ("Opportunity", "add_to_multiselect", "Pain_Points__c"),
    "feature_request": ("Product_Feedback__c", "create_record", "Feature__c"),
    "buying_signal": ("Task", "create_task", "Follow up on buying signal"),
    "content_opportunity": ("Task", "create_task", "Send requested content"),
    "churn_risk": ("Task", "create_task", "CSM: churn risk review"),
    "expansion_opportunity": ("Task", "create_task", "AM: scope expansion"),
}


def idempotency_key(call_id: str, signal: dict) -> str:
    raw = f"{call_id}|{signal['type']}|{signal['value']}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def to_operations(call: dict, signals: list[dict]) -> list[dict]:
    ops = []
    for s in signals:
        obj, action, target = FIELD_MAP[s["type"]]
        ops.append({
            "idempotency_key": idempotency_key(call["call_id"], s),
            "object": obj,
            "account": call["account"],
            "action": action,
            "target": target,
            "value": s["value"],
            "source_call": call["call_id"],
            "evidence": s["evidence"],
            "confidence": s["confidence"],
        })
    return ops
