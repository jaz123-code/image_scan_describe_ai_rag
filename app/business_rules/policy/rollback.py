from fastapi import APIRouter, Form, HTTPException, Depends
from sqlalchemy.orm import Session

from app.business_rules.policy.model import SystemPolicy2
from app.models.dependencies import get_db

api_router = APIRouter(prefix="/api/policy", tags=["policy"])


@api_router.post("/policy-rollback/")
async def rollback_policy(
    key: str = Form(...),
    version: int = Form(...),
    db: Session = Depends(get_db)
):
    target = (
        db.query(SystemPolicy2).filter(SystemPolicy2.key == key, SystemPolicy2.version == version).first()
    )
    if not target:
        raise HTTPException(status_code=404, detail="Policy version not found")
    
    db.query(SystemPolicy2).filter(SystemPolicy2.key == key).update({"is_active": False})

    target.is_active = True
    db.commit()
    return {
        "message": "Policy rolled back",
        "key": key,
        "version": version
    }
