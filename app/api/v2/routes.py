from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import json
from app.services.db.models import image
from app.auth.auth import get_current_user
from app.models.dependencies import get_db

api_router = APIRouter(prefix="/api/v2", tags=["v2"])

@api_router.get("/scan-status/{scan_id}")
async def scan_status_v2(scan_id: str, db: Session=Depends(get_db),current_user=Depends(get_current_user)):
    record=(
        db.query(image).filter(image.image_id==scan_id, image.user_id==current_user.id).first()
    )
    if not record:
        return {"error", "Scan not Found"}
     # ✅ v2 returns full enriched data
    return json.loads(record.image_content)