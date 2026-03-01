from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog
from app.models.dependencies import get_db
from app.dependencies.rate_limit import rate_limit_dependency
from app.auth.auth import get_current_user

api_router = APIRouter(prefix="/audit-logs-v1", tags=["v1"])

@api_router.get("/audit-logs/{scan_id}", dependencies=[Depends(rate_limit_dependency)])
async def get_audit_logs(scan_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    logs = (
        db.query(AuditLog)
        .filter(AuditLog.scan_id == scan_id)
        .order_by(AuditLog.created_at)
        .all()
    )

    return [
        {
            "event_type": log.event_type,
            "message": log.message,
            "created_at": log.created_at
        }
        for log in logs
    ]
