import json

def extract_fields(scan_result_json: str)->dict:
    """
    Extract AI fields from stored scan_result JSON
    """
    data=json.loads(scan_result_json)
    return{
        field: info.get("value")
        for field, info in data.get("fields", {}).items()
        }
    