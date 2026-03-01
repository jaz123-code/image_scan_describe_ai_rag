from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.rate_limit import RateLimit
from app.config.rate_limit import RATE_LIMIT, RATE_WINDOW_SECONDS

def check_rate_limit(db: Session, key: str):
    now=datetime.utcnow()
    record=db.query(RateLimit).filter(RateLimit.key==key).first()
    if not record:
        record=RateLimit(key=key, count=1)
        db.add(record)
        db.commit()
        return
    
    window_end=record.window_start+timedelta(seconds=RATE_WINDOW_SECONDS)
    if now> window_end:
        record.count=1
        record.window_start=now
        db.commit()
        return 
    if record.count>=RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Too many requests .Please try again later"
        )
    record.count+=1
    db.commit()