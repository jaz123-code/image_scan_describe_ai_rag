from .config import ROUTING_POLICY
from .main_router import get_vision_engine
from app.services.calculate_cost import calculate_cost

def run_with_routing(image_path: str, calibration_lookup):
    """
    calibration_lookup(confidence) → actual_accuracy
    """
    #run cheap model
    cheap_cfg=ROUTING_POLICY["cheap_model"]
    cheap_engine=get_vision_engine(cheap_cfg["provider"])
    cheap_result=cheap_engine.analyze(image_path)

    predicted_confidence=cheap_result.get("confidence", 0.0)
    calibrated_accuracy= calibration_lookup(predicted_confidence)
    if calibrated_accuracy>=cheap_cfg["min_calibrated_confidence"]:
        return {
            "result": cheap_result,
            "used_model": cheap_cfg["provider"],
            "escalated": False
        }
    
    #escalate to strong model
    strong_cfg=ROUTING_POLICY["strong_model"]
    strong_engine=get_vision_engine(strong_cfg["provider"])
    strong_result=strong_engine.analyze(image_path)
    return {
        "result": strong_result,
        "used_model": strong_cfg["provider"],
        "escalated": True
    }