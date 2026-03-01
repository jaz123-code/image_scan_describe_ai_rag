from sqlalchemy.orm import Session
from app.business_rules.policy.learning import learn_auto_approval_threshold
from app.business_rules.policy.model import SystemPolicy2
from app.business_rules.policy.update import save_new_policy_version


def update_auto_approval_policy(
    db: Session,
    records: list,
    target_accuracy: float = 0.90
):
    """
    records: List[(confidence: float, is_correct: bool)]

    Learns a new threshold and stores it as a NEW policy version
    """

    # 1️⃣ Learn threshold from data
    new_threshold = learn_auto_approval_threshold(
        records,
        target_accuracy
    )

    # 2️⃣ Save as a NEW VERSION (no overwrite)
    policy = save_new_policy_version(
        db,
        key="auto_approval_threshold",
        value=new_threshold
    )

    return {
        "key": policy.key,
        "value": float(policy.value),
        "version": policy.version,
        "active": policy.is_active
    }


