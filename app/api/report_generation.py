from fastapi import Form, HTTPException, Depends, APIRouter
from fastapi.responses import FileResponse
import os
import json
from sqlalchemy.orm import Session

from app.services.db.models import image
from app.models.dependencies import get_db
from app.auth.auth import get_current_user
from app.dependencies.rate_limit import rate_limit_dependency
from app.services.report_service import create_report
from app.services.audit_logger import log_event

api_router = APIRouter(prefix="/report_generator_v1", tags=["v1"])

REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)

@api_router.post("/generate-report/", dependencies=[Depends(rate_limit_dependency)])
async def generate_report(
    scan_id: str = Form(...),
    report_format: str = Form(...),
    current_user: str=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    record = db.query(image).filter(image.image_id == scan_id, image.user_id == current_user.id).first()


    if not record:
        raise HTTPException(status_code=404, detail="Scan ID not found")

    scan_result = json.loads(record.image_content)

    if scan_result["status"] == "PENDING_REVIEW":
        raise HTTPException(
            status_code=403,
            detail="Manual approval required before report generation"
        )

    report_format = report_format.lower()
    output_path = os.path.join(REPORT_DIR, f"{scan_id}.{report_format}")

    create_report(
        data=scan_result,
        format=report_format,
        output_path=output_path
    )
    log_event(
        db,
        scan_id,
        "REPORT_GENERATED",
        f"Report format={report_format}")
    

    return FileResponse(
        path=output_path,
        filename=f"AI_Report_{scan_id}.{report_format}",
        media_type="application/octet-stream"
    )
