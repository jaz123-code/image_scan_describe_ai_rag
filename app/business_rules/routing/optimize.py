from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.dependencies import get_db
from app.business_rules.routing.optimizer import optimize_routing_threshold

api_router = APIRouter(prefix="/api/routing", tags=["routing"])

@api_router.post("/optimize-routing/")
async def optimize_routing(db: Session = Depends(get_db)):
    rows = db.execute("""
        SELECT
            json_extract(images.image_content, '$.confidence') AS confidence,
            json_extract(images.image_content, '$.routing.model') AS model,
            json_extract(images.image_content, '$.cost.amount') AS cost,
            evaluation_results.result AS result
        FROM images
        JOIN evaluation_results
        ON images.image_id = evaluation_results.scan_id
    """).fetchall()
    records = []
    for row in rows:
        records.append({
            "confidence": float(row[0]),
            "cheap_correct": row[3] == "CORRECT",
            "Strong_correct": row[3] == "CORRECT",
            "cheap_cost": float(row[2]),
            "Strong_cost": float(row[2]) * 5
        })
    best_threshold = optimize_routing_threshold(records)
    return {
        "optimal_routing_threshold": best_threshold
    }
