CONFIDENCE_BUCKETS=[
    (0.0,0.5),
    (0.5,0.6),
    (0.6,0.7),
    (0.7,0.8),
    (0.8,0.9),
    (0.9,1.0),
]

def get_bucket(confidence: float):
    for low, high in CONFIDENCE_BUCKETS:
        if low<=confidence<high:
            return f"{low}-{high}"
    return  "UNKNOWN"
