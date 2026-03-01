def calculate_confidence(extracted_data: dict) -> dict:
    fields = {}
    scores = []

    for key, value in extracted_data.items():
        if not value:
            confidence = 0.2
        elif len(str(value)) < 3:
            confidence = 0.4
        else:
            confidence = 0.8

        fields[key] = {
            "value": value,
            "confidence": confidence
        }
        scores.append(confidence)

    overall_confidence = round(sum(scores) / len(scores), 2) if scores else 0.0

    return fields, overall_confidence
