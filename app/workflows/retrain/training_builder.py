import json
import os
from datetime import datetime
from sqlalchemy import text

from app.models.training_dataset import TrainingDataset
from app.models.Evaluation import Evaluation

DATA_SET = "datasets"
os.makedirs(DATA_SET, exist_ok=True)


def safe_json_load(data):
    try:
        return json.loads(data)
    except:
        return {}


def build_training_dataset(db):

    # -----------------------------------
    # FETCH DATA
    # -----------------------------------
    feedback_rows = db.execute(text("""
        SELECT original_output, corrected_output
        FROM scan_feedback
    """)).fetchall()

    records = db.query(Evaluation).all()

    training_data = []

    X = []
    y = []

    # -----------------------------------
    # PROCESS EVALUATION DATA (FOR MODEL)
    # -----------------------------------
    for record in records:
        if getattr(record, 'confidence', None) is not None and getattr(record, 'actual_status', None) is not None:

            features = [
                record.confidence
            ]

            label = 1 if record.actual_status.upper() == "CORRECT" else 0

            X.append(features)
            y.append(label)

            training_data.append({
                "type": "evaluation",
                "input": {
                    "confidence": record.confidence,
                    "predicted_status": getattr(record, 'predicted_status', None)
                },
                "target": {
                    "is_correct": label
                }
            })

    # -----------------------------------
    # PROCESS FEEDBACK DATA (OPTIONAL STORAGE)
    # (not used for classification yet)
    # -----------------------------------
    for row in feedback_rows:
        training_data.append({
            "type": "correction",
            "input": safe_json_load(row[0]),
            "target": safe_json_load(row[1])
        })

    # -----------------------------------
    # NO DATA SAFETY
    # -----------------------------------
    if not X:
        return None

    # -----------------------------------
    # SAVE DATASET (for audit / retraining history)
    # -----------------------------------
    filename = f"dataset_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    file_path = os.path.join(DATA_SET, filename)

    with open(file_path, 'w') as f:
        json.dump(training_data, f, indent=2)

    dataset_record = TrainingDataset(
        file_path=file_path,
        record_count=len(training_data)
    )

    db.add(dataset_record)
    db.commit()

    # -----------------------------------
    # RETURN ML-READY DATA
    # -----------------------------------
    return {
        "file_path": file_path,
        "records": len(training_data),
        "X": X,
        "y": y
    }