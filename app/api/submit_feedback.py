import uuid
from fastapi import APIRouter, Form, HTTPException, Depends
from sqlalchemy.orm import Session

from app.services.db.models import image
from app.models.dependencies import get_db
from app.auth.auth import get_current_user
from app.models.feedback import ScanFeedback

api_router = APIRouter(prefix="/api/feedback", tags=["feedback"])

@api_router.post("/submit-feedback/")
async def submit_feedback(
    scan_id: str = Form(...),
    corrected_output: str = Form(...),
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

    feedback = ScanFeedback(
        id=str(uuid.uuid4()),
        scan_id=scan_id,
        user_id=current_user.id,
        original_output=record.image_content,
        corrected_output=corrected_output
    )

    db.add(feedback)
    db.commit()

    return {"message": "Feedback saved successfully"}
