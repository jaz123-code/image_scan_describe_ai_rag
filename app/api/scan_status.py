import json
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.services.db.models import image
from app.models.dependencies import get_db
from app.auth.auth import get_current_user
from app.models.feedback import ScanFeedback
from app.business_rules.evaluation.model import Evaluation
from app.business_rules.evaluation.utils import extract_fields
from app.business_rules.evaluation.fields import evaluate_fields

api_router = APIRouter(prefix="/scan-status-v1", tags=["v1"])

@api_router.post("/evaluate-scan/{scan_id}")
async def evaluate_scan(
    scan_id: str,
    db: Session= Depends(get_db)
):
    feedback=db.query(ScanFeedback).filter(ScanFeedback.scan_id==scan_id).first()
    Image=db.query(image).filter(image.image_id==scan_id).first()
    if not feedback or not Image:
        raise HTTPException(status_code=404, detail="Scan not found")
    ai_fields=extract_fields(feedback.original_output)
    human_fields=json.loads(feedback.corrected_output)
    evaluation = evaluate_fields(ai_fields, human_fields)

    for field, result in evaluation.items():
        db.add(
            Evaluation(
                id=str(uuid.uuid4()),
                scan_id=scan_id,
                field=field,
                result=result
            )
        )

    db.commit()

    return {
        "scan_id": scan_id,
        "evaluation": evaluation
    }