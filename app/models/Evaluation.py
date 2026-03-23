"""Evaluation model for tracking scan accuracy and field-level results."""

from sqlalchemy import Column, String, Float, Integer
from app.services.db.models import Base


class Evaluation(Base):
    """
    Model for storing evaluation results of specific scan fields.
    
    Attributes:
        id (str): Unique identifier
        scan_id (str): Reference to the original scan
        field (str): The specific data field evaluated
        result (str): Evaluation outcome (e.g., CORRECT, INCORRECT, PARTIAL)
    """
    __tablename__ = "evaluations"
    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(String, index=True)
    Confidence=Column(Float)
    predicted_status=Column(String)
    actual_status=Column(String)

