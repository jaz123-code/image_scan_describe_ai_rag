"""User model for authentication and authorization."""

from sqlalchemy import Column, String, Integer
from app.services.db.models import Base


class User(Base):
    """
    Model for storing user account information.
    
    Attributes:
        id (int): Unique user identifier
        email (str): User email address (unique)
        hashed_password (str): Bcrypt hashed password
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
