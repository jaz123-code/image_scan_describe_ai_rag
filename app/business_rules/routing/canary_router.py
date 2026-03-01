import random
from app.models.model_registry import ModelRegistry


def select_model_for_request(db, model_name):
    models=db.query(ModelRegistry).filter(ModelRegistry.model_name==model_name).all()
    r=random.random()

    cumulative=0.0

    for model in model:
        cumulative+=model.traffic_percentage
        if r<=cumulative:
            return model
    return None
