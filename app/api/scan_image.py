import os
import uuid
import shutil
import json
from fastapi import APIRouter, Depends, Form, UploadFile, File, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session

from app.services.db.models import image
from app.auth.auth import get_current_user
from app.models.dependencies import get_db
from app.dependencies.rate_limit import rate_limit_dependency
from app.services.file_validator import validate_image
from app.business_rules.policy.service import get_policy
from app.services.audit_logger import log_event
from app.workflows.scan.scan_task import run_scan_task
from app.infrastructure.celery_app import celery_app


api_router = APIRouter(prefix="/api-v1", tags=["v1"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@api_router.post("/scan-image/", dependencies=[Depends(rate_limit_dependency)])
async def scan_image_api(
    background_tasks: BackgroundTasks,
    image_file: UploadFile = File(...),
    provider: str = Form(...),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 🔐 File security
    validate_image(image_file)

    image_id = str(uuid.uuid4())
    image_path = os.path.join(UPLOAD_DIR, f"{image_id}_{image_file.filename}")

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image_file.file, buffer)

    # 🔹 Fetch learned policy (AUTO-TUNED)
    auto_approval_threshold = get_policy(
        db,
        key="auto_approval_threshold",
        default=0.75
    )

    # 🔹 Initial DB record
    record = image(
        image_id=image_id,
        user_id=current_user.id,
        image_content=json.dumps({"status": "PROCESSING"})
    )

    db.add(record)
    db.commit()

    log_event(
        db,
        image_id,
        "SCAN_STARTED",
        f"provider={provider}, threshold={auto_approval_threshold}"
    )
    queue_name="high_priority" if current_user.is_premium else "default"
    # 🔹 Background AI scan
    task=run_scan_task.apply_async(
        args=[image_id, image_path, provider, auto_approval_threshold],
        queue=queue_name
    )
    task_id=task.id
    result=celery_app.AsyncResult(task_id)
    print(task_id)
    print(task_id.status)

    
