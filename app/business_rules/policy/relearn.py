
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.dependencies import get_db
from app.business_rules.policy.updater import update_auto_approval_policy
from sqlalchemy import text

api_router = APIRouter(prefix="/relearn-policy", tags=["policy-v1"])

@api_router.post("/relearn-policy/")
async def relearn_policy(db: Session=Depends(get_db)):
    query = text("""
        SELECT
            json_extract(images.image_content, '$.confidence') AS confidence,
            CASE
                WHEN evaluation_results.result = 'CORRECT' THEN 1
                ELSE 0
            END AS is_correct
        FROM images
        JOIN evaluation_results
        ON images.image_id = evaluation_results.scan_id
        WHERE json_extract(images.image_content, '$.confidence') IS NOT NULL;
    """)
    rows = db.execute(query).fetchall()
    records=[
        (row[0], bool(row[1]))
         for row in rows 
         if row[0] is not None
    ]
    if not records:
        raise HTTPException(status_code=400, detail="No valid records found for policy learning")
    new_threshold=update_auto_approval_policy(db,records)
    return{
        "message": "Policy updated successfully",
        "auto_approval_threshold": new_threshold
    }