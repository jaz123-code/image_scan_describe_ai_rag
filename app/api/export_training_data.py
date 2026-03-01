from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.dependencies import get_db
from app.workflows.retrain.training_builder import build_training_dataset

api_router = APIRouter(prefix="/api/admin", tags=["admin"])

@api_router.post("/export-training-data/")
async def export_training_data(db: Session = Depends(get_db)):
    result = build_training_dataset(db)

    if not result:
        raise HTTPException(
            status_code=400,
            detail="No feedback data available"
        )
    return {
        "message": "Training dataset created",
        "file_path": result["file_path"],
        "records": result["records"]
    }
