from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.dependencies import get_db
from app.services.db.models import image 

router = APIRouter(prefix="/api/v1", tags=["scan-history"])

@router.get("/scans")
def get_scan_history(db: Session= Depends(get_db)):
    scans=db.query(image).order_by(image.created_at.desc()).all()

    results=[]
    for scan in scans:
        results.append({
            "image_id": scan.image_id,
            "filename": scan.filename,
            "status": scan.status,
            "progress": scan.progress,
            "created_at": scan.created_at
        })
    return {"scans": results}

