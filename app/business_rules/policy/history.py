from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.dependencies import get_db
from app.business_rules.policy.model import SystemPolicy2

api_router = APIRouter(prefix="/api/policy", tags=["policy"])

@api_router.post("/policy-history/{key}")
async def policy_history(key: str, db: Session = Depends(get_db)):
    policies = (
        db.query(SystemPolicy2).filter(SystemPolicy2.key == key).order_by(SystemPolicy2.version.desc()).all()
    )
    return [
        {
            "version": p.version,
            "value": p.value,
            "is_active": p.is_active,
            "created_at": p.created_at

        }
        for p in policies
    ]
