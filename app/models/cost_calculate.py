"""Cost tracking model for managing scan expenses."""

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from app.services.db.models import image, Base


class CostHistory(Base):
    """
    Model for tracking costs associated with each image scan.
    
    Attributes:
        id (int): Unique identifier
        image_id (str): Foreign key reference to the image model
        cost (float): Cost of processing the image
        currency (str): Currency code (e.g., USD)
        image: Relationship to the Image model
    """
    __tablename__ = "cost_history"
    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(String, ForeignKey("image.image_id"))
    cost = Column(Float, nullable=False)
    currency = Column(String)

    # Define the relationship to the Image model
    image = relationship("image")
