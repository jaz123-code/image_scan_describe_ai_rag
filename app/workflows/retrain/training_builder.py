import json
import os
from datetime import datetime
from app.models.training_dataset import TrainingDataset


DATA_SET="datasets"
os.makedirs(DATA_SET, exist_ok=True)

def build_training_dataset(db):
    rows=db.execute("""
        SELECT scan_feedback.original_output,
               scan_feedback.corrected_output
        FROM scan_feedback
    """).fetchall()

    training_data=[]

    for row in rows:
        training_data.append({
            "input": json.loads(row[0]),
            "target": json.loads(rows[1])
        })
    if not training_data:
        return None
    filename=f"dataset_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    file_path=os.path.join(DATA_SET, filename)

    with open(file_path, 'w') as f:
        json.dump(training_data, f, indent=2)

    dataset_record=TrainingDataset(
        file_path=file_path,
        record_count=len(training_data)
    )
    db.add(dataset_record)
    db.commit()

    return {
        "file_path": file_path,
        "records": len(training_data)
    }
