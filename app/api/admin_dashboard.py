from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.dependencies import get_db
from app.auth.auth import get_current_user
from app.services.admin_dashboard import (
    build_system_summary,
    get_active_policies
)

api_router = APIRouter(prefix="/api/admin", tags=["admin"])

@api_router.get("/admin-dashboard/")
async def admin_dashboard(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # You may later add admin-role check here
    summary = build_system_summary(db)
    policies = get_active_policies(db)
    return {
        "system_summary": summary,
        "active_policies": policies
    }
