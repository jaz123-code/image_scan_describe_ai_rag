from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.dependencies import get_db
from app.auth.auth import get_current_user
from app.services.alert_engine import evaluate_system_health, store_alerts

api_router = APIRouter(prefix="/api/admin", tags=["admin"])

@api_router.post("/run-health-check/")
async def run_health_check(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    alerts = evaluate_system_health(db)
    if alerts:
        store_alerts(db, alerts)
    return {
        "alerts_detected": alerts
    }
