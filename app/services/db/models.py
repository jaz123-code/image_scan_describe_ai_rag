"""
Core SQLAlchemy models and database configuration.

This module defines:
- Base class for all models
- Core Image model for storing scan results
"""

from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Boolean

Base = declarative_base()


class image(Base):
    """
    Image model for storing scan information and results.
    
    Attributes:
        image_id (str): Unique identifier for the scan (primary key)
        user_id (str): ID of the user who initiated the scan (indexed for queries)
        image_content (str): JSON string containing scan results and metadata
    """
    __tablename__ = "image"
    image_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    image_content = Column(String, nullable=False)



