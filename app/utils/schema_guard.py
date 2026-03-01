REQUIRED_SCHEMA={"document_type", "extracted_data", "summary"}

def enforce_schema(data: dict)->dict:
    if not isinstance(data, dict):
        raise ValueError("Invalid AI response")
    missing=REQUIRED_SCHEMA-data.keys()
    if missing:
         raise ValueError(f"Missing keys: {missing}")
    return data