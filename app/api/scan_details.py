from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
from app.models.dependencies import get_db
from app.services.db.models import image
from app.auth.auth import get_current_user
router = APIRouter(prefix="/api-v1", tags=["scan-details"])

@router.get("/scan-details/{image_id}")
def get_scan_details(image_id: str, db: Session=Depends(get_db), current_user=Depends(get_current_user)):
    records=(
        db.query(image).filter(image.image_id==image_id, image.user_id==current_user.id).first()
    )
    if not records:
        raise HTTPException(status_code=404, detail="Scan not found")

    try:
        data = json.loads(records.image_content) if records.image_content else {}
    except json.JSONDecodeError:
        data = {"raw": records.image_content}

    return {
        "image_id": records.image_id,
        "filename": records.filename,
        "status": data.get("status", ""),
        "confidence": data.get("confidence", ""),
        "fields": data.get("fields", {}),
        "summary": data.get("summary", ""),
        "warnings": data.get("warnings", []),
        "active_learning": data.get("active_learning", {}),
        "routing": data.get("routing", {}),
    }