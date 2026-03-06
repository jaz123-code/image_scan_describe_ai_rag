from celery import Celery
from kombu import Queue
celery_app=Celery(
    "ai_platform",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)
celery_app.conf.task_routes={
    Queue("High_priority"),
    Queue("default"),
    Queue("low_priority")
}
celery_app.conf.task_default_queue="default"