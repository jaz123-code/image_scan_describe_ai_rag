"""System alert model for monitoring health and issues."""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.services.db.models import Base


class SystemAlert(Base):
    """
    Model for storing system alerts and health notifications.
    
    Attributes:
        id (int): Unique identifier
        type (str): Alert type (e.g., HIGH_COST, LOW_ACCURACY)
        message (str): Alert message
        severity (str): Severity level (INFO, WARNING, CRITICAL)
        created_at (datetime): When the alert was generated
    """
    __tablename__ = "system_alerts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String)
    message = Column(String)
    severity = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    