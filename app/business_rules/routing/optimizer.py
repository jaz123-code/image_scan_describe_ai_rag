def optimize_routing_threshold(records, lambda_cost=1.0):
    """
    records:
        [
            {
                "confidence": float,
                "cheap_correct": bool,
                "strong_correct": bool,
                "cheap_cost": float,
                "strong_cost": float
            }
        ]
    """
    best_threshold=0.75
    best_score=float('-inf')
    for threshold in [x/100 for x in range(50, 96, 2)]:
        total_utility=0
        for r in records:
            if r["confidence"]>=threshold:
                #use cheap model
                accuracy=1 if r["cheap_correct"] else 0
                cost= r["cheap_cost"]
            else:
                #escalate
                accuracy=1 if r["strong_correct"] else 0
                cost=r["strong_cost"]
            utility=accuracy-(lambda_cost*cost)
            total_utility+=utility
        if total_utility>best_score:
            best_score=total_utility
            best_threshold=threshold
    return round(best_threshold, 2)

