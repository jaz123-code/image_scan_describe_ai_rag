import json
from sqlalchemy.orm import Session
from app.services.db.models import image

def update_progress(db: Session, scan_id: str, *, status: str= "PROCESSING", progress: int, stage: str, message: str=""):
    record=db.query(image).filter(image.image_id==scan_id).first()
    if not record:
        return 
    record.scan_result=json.dumps({
        "status": status,
        "progress": progress,
        "stage": stage,
        "message": message
    })
    db.commit()
    