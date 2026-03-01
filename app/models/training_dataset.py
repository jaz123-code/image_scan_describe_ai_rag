"""Training dataset model for managing machine learning datasets."""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.services.db.models import Base


class TrainingDataset(Base):
    """
    Model for tracking training datasets created from user feedback.
    
    Attributes:
        id (int): Unique identifier
        file_path (str): Path to the dataset file
        record_count (int): Number of records in the dataset
        created_at (datetime): When the dataset was created
    """
    __tablename__ = "training_datasets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_path = Column(String)
    record_count = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    