

def build_system_summary(db):
    summary={}
    # Total scans
    total_scans=db.execute("SELECT COUNT(*) FROM images").scalar()

    #Auto approved
    auto_count=db.execute("""
        SELECT COUNT(*) FROM images 
        WHERE json_extract(image_content,  '$.status')= 'AUTO_APPROVED""").scalar()
    pending_count=db.execute("""
        SELECT COUNT(*) FROM images
        WHERE json_sxtract(image_content, '$.status)='PENDING_REVIEW""").scalar()
    # Failed
    failed_count = db.execute("""
        SELECT COUNT(*) FROM images
        WHERE json_extract(image_content, '$.status') = 'FAILED'
    """).scalar()
       # Total cost
    total_cost = db.execute("""
        SELECT SUM(cost) FROM cost_history
    """).scalar() or 0

    summary["total_scans"]=total_scans
    summary["auto_approved"]=auto_count
    summary["pending_review"]=pending_count
    summary["failed"]=failed_count
    summary["total_cost"]=round(total_cost, 2)

    if total_scans:
        summary["auto_approval_rate"]=round(auto_count/total_scans,2)
        summary["review_rate"]=round(pending_count/total_scans,2)
    else:
        summary["auto-approval_rate"]=0
        summary["review_rate"]=0
    return summary

def get_active_policies(db):
    row=db.execute("""
        SELECT key,value, version FROM system_policies 
        WHERE is_active=1""").fetchall()
    return [
        {
            "key": r[0],
            "value": r[1],
            "version": r[2]
        }
        for r in row

    ]