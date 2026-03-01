def calibration_lookup(confidence: float)->float:
    """
    Maps predicted confidence → real accuracy
    (based on your calibration stats)
    """
    if confidence>=0.9:
        return 0.93
    if confidence >=0.8:
        return 0.84
    if confidence >=0.7:
        return 0.71
    return 0.5