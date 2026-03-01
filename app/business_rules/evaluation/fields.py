def evaluate_fields(ai_fields: dict, human_fields: dict)->dict:
    results={}
    for field, ai_value in ai_fields.items():
        human_value=human_fields.get(field)
        if human_value is None:
            results[field]="MISSING_GROUND_TRUTH"
        elif ai_value==human_value:
            results[field]="CORRECT"
        else:
            results[field]="INCORRECT"
    return results