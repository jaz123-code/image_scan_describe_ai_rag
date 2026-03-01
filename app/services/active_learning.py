from app.config.active_learning import ACTIVE_LEARNING_CONFIG

def should_request_human_review(scan_result: dict)->dict:
    reasons=[]
    confidence=scan_result.get("confidence", 0)
    if confidence < ACTIVE_LEARNING_CONFIG["min_calibrated_confidence"]:
        reasons.append("LOW_CONFIDENCE")
    routing=scan_result.get("routing", {})
    if routing.get("escalated"):
        reasons.append("MODEL_ESCALATED")
    fields=scan_result.get('fields', {})
    confidences=[]
    for field, info in fields.items():
        field_conf=info.get("confidence", 0)
        confidences.append(field_conf)

        if field in ACTIVE_LEARNING_CONFIG["important_fields"] and field_conf < 0.8:
            reasons.append(f"IMPORTANT_FIELD_LOW_CONF: {field}")
    if confidences:
        gap=max(confidences)-min(confidences)
        if gap> ACTIVE_LEARNING_CONFIG["max_field_confidence_gap"]:
            reasons.append("HIGH_CONFIDENCE_VARIANCE")
    return {
        "request_review": len(reasons)>0,
        "reasons": reasons
    }