"""System policy model for auto-tuning configuration."""

from sqlalchemy import Column, String, DateTime, Integer, Boolean
from sqlalchemy.sql import func
from app.models.models import Base


class SystemPolicy(Base):
    """
    Legacy policy model (see SystemPolicy2 for current version).
    
    Attributes:
        key (str): Policy key (primary key)
        value (str): Policy value
        updated_at (datetime): Last update timestamp
    """
    __tablename__ = "system_policy"

    key = Column(String, primary_key=True)
    value = Column(String)
    updated_at = Column(DateTime, default=func.now())


class SystemPolicy2(Base):
    """
    Enhanced system policy model with versioning support.
    
    Attributes:
        id (int): Unique identifier
        key (str): Policy key
        value (str): Policy value
        version (int): Policy version number
        is_active (bool): Whether this version is currently active
        created_at (datetime): When this policy version was created
    """
    __tablename__ = "system_policy2"
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String, index=True)
    value = Column(String)
    version = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    


