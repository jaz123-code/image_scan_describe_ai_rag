import json
from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from app.services.db.models import image
from app.models.dependencies import get_db
from app.auth.auth import get_current_user
from app.services.audit_logger import log_event

api_router = APIRouter(prefix="/api-v1", tags=["v1"])

@api_router.post("/human-approval/")
async def human_approval(
    scan_id: str = Form(...),
    approve: bool = Form(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    record = (
        db.query(image)
        .filter(image.image_id == scan_id, image.user_id == current_user.id)
        .first()
    )

    if not record:
        raise HTTPException(status_code=404, detail="Scan ID not found")

    scan_result = json.loads(record.image_content)

    new_status = "HUMAN_APPROVED" if approve else "REJECTED"
    scan_result["status"] = new_status

    log_event(
        db,
        scan_id,
        new_status,
        "Scan reviewed by human reviewer"
    )

    record.image_content = json.dumps(scan_result)
    db.commit()

    return {
        "scan_id": scan_id,
        "new_status": new_status
    }
