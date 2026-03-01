def analyze_performance(records):
    """
    records: list of dicts:
        {
            "model": str,
            "cost": float,
            "is_correct": bool
        }
    """
    stats={}

    for r in records:
        model=r["model"]
        if model not in stats:
            stats[model]={
                "total": 0,
                "correct": 0,
                "total_cost": 0
            }
        stats[model]["total"]+=1
        stats[model]["total_cost"]+=r["cost"]

        if r["is_correct"]:
            stats[model]["correct"]+=1
    for model in stats:
        s=stats[model]
        s["acccuracy"]=s["correct"]/s["total"]
        s["avg_cost"]=s["total_cost"]/s["total"]
        s['cost_per_correct']=(
            s["total_cost"]/s["correct"]
            if s["correct"]>0 else None
        )
    return stats
