from celery import Celery
from kombu import Queue

celery_app = Celery(
    "ai_platform",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=['app.workflows.scan.scan_task']
)

# Define available queues explicitly; routing is handled via queue names in apply_async
celery_app.conf.task_queues = (
    Queue("high_priority"),
    Queue("default"),
    Queue("low_priority"),
)
celery_app.conf.task_default_queue = "default"