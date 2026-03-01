"""Evaluation results model for tracking model accuracy metrics."""

from sqlalchemy import Column, String
from app.services.db.models import Base


class Evaluation(Base):
    """
    Model for storing field-level evaluation results.
    
    Attributes:
        id (str): Unique identifier
        scan_id (str): Reference to the scan being evaluated
        field (str): Name of the extracted field
        result (str): Evaluation result (CORRECT, INCORRECT, PARTIAL)
    """
    __tablename__ = "evaluation_results"
    id = Column(String, primary_key=True)
    scan_id = Column(String, index=True)
    field = Column(String, index=True)
    result = Column(String)