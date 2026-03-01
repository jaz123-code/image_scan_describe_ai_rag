from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.db.models import image
from app.business_rules.evaluation.model import Evaluation
from app.models.dependencies import get_db
from app.services.calibration_stats import build_calibration_stats


api_router = APIRouter(prefix="/calibration-report", tags=["v1"])


@api_router.get("/calibration-report/")
async def calibration_report(db: Session = Depends(get_db)):
    rows = db.query(
        image.image_content['confidence'].as_float(),
        Evaluation.result
    ).join(Evaluation, image.image_id == Evaluation.scan_id).all()
    
    records = [(confidence, result == 'CORRECT') for confidence, result in rows if confidence is not None]
    stats=build_calibration_stats(records)
    return stats