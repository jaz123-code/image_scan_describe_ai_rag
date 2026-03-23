import uuid
import json
from fastapi import APIRouter, Form, HTTPException, Depends
from sqlalchemy.orm import Session

from app.services.db.models import image
from app.models.dependencies import get_db
from app.auth.auth import get_current_user
from app.models.feedback import ScanFeedback
from app.models.Evaluation import Evaluation

api_router = APIRouter(prefix="/api/feedback", tags=["feedback"])


@api_router.post("/submit-feedback/")
async def submit_feedback(
    scan_id: str = Form(...),
    corrected_output: str = Form(...),
    is_correct: bool = Form(...),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    record = (
        db.query(image)
        .filter(image.image_id == scan_id, image.user_id == current_user.id)
        .first()
    )

    if not record:
        raise HTTPException(status_code=404, detail="Scan not found")

    # -----------------------------------
    # PARSE ORIGINAL RESULT
    # -----------------------------------
    try:
        original_data = json.loads(record.image_content or "{}")
    except json.JSONDecodeError:
        original_data = {}

    confidence = original_data.get("confidence", 0.0)
    predicted_status = original_data.get("status", "UNKNOWN")
    
    # -----------------------------------
    # SAVE FEEDBACK
    # -----------------------------------
    feedback = ScanFeedback(
        id=str(uuid.uuid4()),
        scan_id=scan_id,
        user_id=current_user.id,
        original_output=record.image_content or "{}",
        created_at=None, # Let server_default handle it
        corrected_output=corrected_output
    )

    db.add(feedback)
    eval=db.query(Evaluation).filter(Evaluation.scan_id==scan_id).first()
    if eval:
        eval.actual_status="CORRECT" if is_correct else "Wrong"
        db.commit()


    # -----------------------------------
    # SAVE EVALUATION (VERY IMPORTANT)
    # -----------------------------------
    if not eval:
        evaluation = Evaluation(
        id=str(uuid.uuid4()), # Note: Evaluation model in context doesn't show id as PK, but usually needed
        scan_id=scan_id,
        Confidence=confidence,
        predicted_status=predicted_status,
        actual_status="CORRECT" if is_correct else "INCORRECT",
        )
        db.add(evaluation)
        db.commit()

    return {"message": "Feedback saved successfully"}