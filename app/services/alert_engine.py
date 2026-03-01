from app.models.system_alert import SystemAlert
def evaluate_system_health(db):
    alerts=[]
    #check accuracy
    accuracy_row=db.execute("""
        SELECT AVG(
            CASE WHEN result = 'CORRECT' THEN 1 ELSE 0 END
        )
        FROM evaluation_results
    """).scalar()
    if accuracy_row is not None and accuracy_row< 0.85:
        alerts.append({
            "type": "ACCURACY_DROP",
            "message": f"System accuracy dropped to {round(accuracy_row, 2)}",
            "severity": "CRITICAL"
        })
    #check cost cost spike
    cost_row=db.execute("""
        SELECT SUM(cost) FROM cost_history
    """).scalar() or 0
    if cost_row>1000:
        alerts.append({
             "type": "COST_SPIKE",
            "message": f"Total cost exceeded threshold: {cost_row}",
            "severity": "WARNING"
        })
    return alerts
#Store alerts in db
def store_alerts(db,alerts):
    for alert in alerts:
        new_data=SystemAlert(
            type=alert["type"],
            message=alert["message"],
            severity=alert["severity"]

        )
        db.add(new_data)
        db.commit()
        db.refresh(new_data)

