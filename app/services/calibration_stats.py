from collections import defaultdict
from app.services.calibration import get_bucket

def build_calibration_stats(records):
    """
    records: list of tuples (confidence, is_correct)
    """
    buckets=defaultdict(lambda: {"correct": 0, "total": 0})
    for confidence, is_correct in records:
        bucket=get_bucket(confidence)
        buckets[bucket]["total"]+=1
        if is_correct:
            buckets[bucket]["correct"]+=1
        for bucket in buckets:
            total=buckets[bucket]["total"]
            buckets[bucket]["accuracy"]=(
                buckets[bucket]["correct"]/total if total else 0
            )
    return buckets