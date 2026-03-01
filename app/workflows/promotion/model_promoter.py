from app.models.model_registry import ModelRegistry

def promote_if_better(db, model_name, new_accuracy):
    current_active=(
        db.query(ModelRegistry).filter(ModelRegistry.model_name==model_name, ModelRegistry.is_active==True).first()
    )

    if not current_active:
        new_model=ModelRegistry(
            model_name=model_name,
            version=1,
            accuracy=new_accuracy,
            traffic_percentage=1.0,
            is_active=True
        )
        db.add(new_model)
        db.commit()
        return "INTIALLY_PROMOTED"
    if new_accuracy>current_active.accuracy:
        current_active.traffic_percentage=0.9
        current_active.is_active=True

        new_model=ModelRegistry(
            model_name=model_name,
            accuracy=new_accuracy,
            traffic_percentage=0.1,
            is_active=False        )
        db.add(new_model)
        db.commit()
        return "CANARY_DEPLOYED"
    return "REJECTED"
