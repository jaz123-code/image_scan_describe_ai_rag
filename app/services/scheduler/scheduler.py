from apscheduler.schedulers.background import BackgroundScheduler
from app.services.alert_engine import evaluate_system_health, store_alerts
from app.models.dependencies import SessionLocal
from app.business_rules.policy.model import SystemPolicy2
from app.business_rules.policy.update import save_new_policy_version
from app.workflows.retrain.training_builder import build_training_dataset
from app.workflows.retrain.training_engine import train_new_model
from app.workflows.promotion.model_promoter import promote_if_better
from app.models.model_registry import ModelRegistry

scheduler=BackgroundScheduler()

def schedule_health_check():
    db=SessionLocal()
    try:
        alerts=evaluate_system_health(db)
        if alerts:
            store_alerts(db, alerts)

            #get current active threshold
            active_policy=(
                db.query(SystemPolicy2).filter(SystemPolicy2.key=="auto_approval_threshold", SystemPolicy2.is_active==True).first()
            )
            current_threshold=(float(active_policy.value) if active_policy else 0.75)

            #get current system accuracy
            accuracy=db.execute(
                """
            SELECT AVG(
                CASE WHEN result = 'CORRECT' THEN 1 ELSE 0 END
            )
            FROM evaluation_results
        """
            ).scalar()
            #tighten threshold
            if accuracy is not None and accuracy < 0.85:
                print("Accuracy Dropped . Tightening threshold")
                if current_threshold<0.95:
                    save_new_policy_version(
                        db,
                        key="auto_approval_threshold",
                        value=0.95
                    )
            #relax threshold gradually if recovered
            elif accuracy is not None and accuracy >0.92:
                print("✅ Accuracy recovered. Relaxing threshold.A")
                if current_threshold>0.80:
                    new_threshold=round(current_threshold-0.02, 2)

                    save_new_policy_version(
                        db,
                        key="auto_approval_threshold",
                        value=new_threshold
                    )
            #optional auto-response
            for alert in alerts:
                if alert["type"]=="COST_SPIKE":
                    print("⚠ Cost spike detected. Raising threshold.")
                    if current_threshold<0.98:
                        save_new_policy_version(
                            db,
                            key="auto_approval_threshold",
                            value=0.98
                        )
    finally:
        db.close()



def scheduled_retraining():
    db=SessionLocal()
    try:
        print("Running scheduled retraining....")
        dataset=build_training_dataset(db)
        if not dataset:
            print("No feedback available for retraining")
            return 
        model_result=train_new_model(dataset["file_path"])

        promotion_status=promote_if_better(
            db,
            model_result["model_name"],
            model_result["accuracy"]
        )
        print(f"retraining result: {promotion_status}")
    finally:
        db.close()

def evaluate_canary_models():
    db=SessionLocal()
    try:
        canary_models=db.query(ModelRegistry).filter(ModelRegistry.traffic_percentage<1.0, ModelRegistry.traffic_percentage>0.0).all()
        for model in canary_models:
            if model.accuracy>0.90:
                print("Promoting canary to full traffic")
                model.traffic_percentage=1.0
                model.is_active=1.0

                #deactivate others
                db.query(ModelRegistry).filter(ModelRegistry.model_name==model.model_name, ModelRegistry.id!=model.id).update({"traffic_percentage: 0.0"})
        db.commit()
    finally:
        db.close()
def start_scheduler():
    if not scheduler.get_job("health_check"):
        scheduler.add_job(
            schedule_health_check,
            "interval",
            minutes=10,
            id="health_check"
        )
    if not scheduler.get_job("model_retraining"):
        scheduler.add_job(
            scheduled_retraining,
            "interval",
            hours=24,
            id="model_retraining"
        )
    if not scheduler.get_job("canary_evaluation"):
        scheduler.add_job(
            evaluate_canary_models,
            "interval",
            hours=6,
            id="canary_evaluation"
        )
    if not scheduler.running:
        scheduler.start()