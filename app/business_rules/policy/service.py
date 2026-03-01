from sqlalchemy.orm import Session
from app.business_rules.policy.model import SystemPolicy2 as system_policy

def get_policy(db: Session, key: str, default=float):
    record=db.query(system_policy).filter(system_policy.key==key, system_policy.is_active==True).first()
    if not record:
        return default
    try:
        return float(record.value)
    except ValueError:
        return default