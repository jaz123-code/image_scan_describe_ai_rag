"""Rate limiting model for API request throttling."""

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from app.services.db.models import Base


class RateLimit(Base):
    """
    Model for tracking rate limit windows per client.
    
    Attributes:
        key (str): Client identifier (usually IP address)
        count (int): Number of requests in current window
        window_start (datetime): Start of the current time window
    """
    __tablename__ = "rate_limits"

    key = Column(String, primary_key=True, index=True)
    count = Column(Integer, default=0)
    window_start = Column(DateTime(timezone=True), server_default=func.now())
