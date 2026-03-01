"""
Audit Log model for tracking system events and user actions.
"""

from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func
from app.services.db.models import Base


class AuditLog(Base):
    """
    Audit log for recording all significant events in the system.
    
    Attributes:
        id (str): Unique identifier for the log entry
        scan_id (str): Reference to the scan that triggered the event
        event_type (str): Type of event (e.g., SCAN_COMPLETED, HUMAN_APPROVED)
        message (str): Detailed message about the event
        created_at (datetime): Timestamp when the event was logged
    """
    __tablename__ = "audit_logs"
    id = Column(String, primary_key=True, index=True)
    scan_id = Column(String, index=True)
    event_type = Column(String, index=True)
    message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
