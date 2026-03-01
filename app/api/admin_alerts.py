from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.dependencies import get_db
from app.auth.auth import get_current_user

api_router = APIRouter(prefix="/api/admin", tags=["admin"])

@api_router.post("/alerts/")
async def get_alerts(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # You may later add admin-role check here
    rows = db.execute("""
        SELECT type, message, severity, created_at
        FROM system_alerts
        ORDER BY created_at DESC
        LIMIT 50
    """).fetchall()
    return [
        {
            "type": row[0],
            "message": row[1],
            'severity': row[2],
            "created_at": row[3]
        }
        for row in rows
    ]
