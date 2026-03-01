from sqlalchemy.orm import Session
from app.business_rules.policy.model import SystemPolicy2

def save_new_policy_version(
        db: Session,
        key: str,
        value: str
):
    #deactivate old versions
    db.query(SystemPolicy).filter(SystemPolicy.key==key,SystemPolicy.is_active==True).update({"is_active": False})
    latest=(
        db.query(SystemPolicy).filter(SystemPolicy.key==key).order_by(SystemPolicy.version.desc()).first()
    )
    new_version=1 if not latest else latest.version+1
    policy=SystemPolicy(
        key=key,
        value=value,
        version=new_version,
        is_active=True
    )
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy
