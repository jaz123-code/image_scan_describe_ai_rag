from app.config.costs import MODEL_COST

def calculate_cost(provider: str, model: str)->float:
    key=f"{provider}:{model}"
    config=MODEL_COST.get(key)
    if not config:
        return 0.0
    return config.get("per_image", 0.0)
