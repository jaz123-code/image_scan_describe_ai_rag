from fastapi import APIRouter, Depends, Form, UploadFile, File
from sqlalchemy.orm import Session
import json
from app.services.db.models import image 
from app.auth.auth import get_current_user
from app.models.dependencies import get_db
from fastapi import HTTPException

api_router = APIRouter(prefix="/api/v1", tags=["v1"])

@api_router.get("/scan-status/{scan_id}")
async def scan_status(scan_id: str, db: Session=Depends(get_db),
                      current_user=Depends(get_current_user)):
    record=(
        db.query(image).filter(image.image_id==scan_id, image.user_id==current_user.id))
    if not record:
        raise HTTPException(status_code=401, detail="Scan not found")
    data=json.loads(record.image_content)
    return {
        "status": data.get("status", ""),
        "message": data.get("confidence", ""),
        "summary": data.get("summary", "N/A")
    }
    