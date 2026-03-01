"""Model registry for tracking deployed AI models and their versions."""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.sql import func
from app.services.db.models import Base


class ModelRegistry(Base):
    """
    Model registry for tracking deployed models and their performance.
    
    Supports canary deployments with traffic splitting.
    
    Attributes:
        id (int): Unique identifier
        model_name (str): Name of the model
        version (int): Version number
        accuracy (float): Model accuracy metric
        traffic_percentage (float): Percentage of traffic routed to this model
        is_active (bool): Whether the model is active
        created_at (datetime): When the model was registered
    """
    __tablename__ = "model_registry"

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String)
    version = Column(Integer)
    accuracy = Column(Float)
    traffic_percentage = Column(Float, default=0.0)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    