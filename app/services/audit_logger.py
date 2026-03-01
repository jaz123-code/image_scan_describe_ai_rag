import uuid
from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog

def log_event(db: Session, scan_id: str, event_type: str, message: str):
    log=AuditLog(id=str(uuid.uuid4()),
                  scan_id=scan_id, 
                  event_type=event_type,
                  message=message)
    db.add(log)
    db.commit()

