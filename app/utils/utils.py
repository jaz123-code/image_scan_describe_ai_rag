import json

def parse_vision_response(raw_response: str)->dict:
    try:
        return json.loads(raw_response)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}
    