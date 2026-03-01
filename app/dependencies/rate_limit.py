from fastapi import Request, Depends
from sqlalchemy.orm import Session
from app.models.dependencies import get_db
from app.services.rate_limiter import check_rate_limit

def rate_limit_dependency(
    request: Request,
    db: Session = Depends(get_db)
):
    client_ip = request.client.host
    check_rate_limit(db, key=client_ip)
