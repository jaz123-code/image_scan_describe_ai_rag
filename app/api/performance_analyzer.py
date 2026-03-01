from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.dependencies import get_db
from app.services.performance_analyzer import analyze_performance

api_router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@api_router.get("/performance-analyzer/")
async def performance_analyzer(db: Session = Depends(get_db)):
    rows = db.execute("""
        SELECT
            json_extract(images.image_content, '$.routing.model') AS model,
            json_extract(images.image_content, '$.cost.amount') AS cost,
            CASE
                WHEN evaluation_results.result = 'CORRECT' THEN 1
                ELSE 0
            END AS is_correct
        FROM images
        JOIN evaluation_results
        ON images.image_id = evaluation_results.scan_id
    """).fetchall()
    records = [
        {
            "model": row[0],
            'cost': float(row[1] or 0),
            "is_correct": bool(row[2])
        }
        for row in rows
        if row[0] is not None
    ]
    stat = analyze_performance(records)
    return stat
