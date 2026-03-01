def validate_scan(fields: dict) -> list:
    warnings = []

    for field, data in fields.items():
        if data["confidence"] < 0.5:
            warnings.append(f"Low confidence for field: {field}")

        if data["value"] in ["", None]:
            warnings.append(f"Missing value for field: {field}")

    return warnings
