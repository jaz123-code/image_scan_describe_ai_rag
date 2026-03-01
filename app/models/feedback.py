"""User feedback model for storing scan corrections and learning data."""

from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.sql import func
from app.services.db.models import Base


class ScanFeedback(Base):
    """
    Model for storing user feedback and corrections to scan results.
    
    Used for active learning to improve model accuracy.
    
    Attributes:
        id (str): Unique identifier
        scan_id (str): Reference to the original scan
        user_id (str): ID of the user providing feedback
        original_output (str): Original AI-generated output (JSON string)
        corrected_output (str): User-corrected output (JSON string)
        created_at (datetime): Timestamp of feedback submission
    """
    __tablename__ = "scan_feedback"

    id = Column(String, primary_key=True, index=True)
    scan_id = Column(String, index=True)
    user_id = Column(String, index=True)
    original_output = Column(Text)
    corrected_output = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
