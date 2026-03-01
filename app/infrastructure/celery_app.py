from celery import Celery

celery_app=Celery(
    "ai_platform",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)
celery_app.conf.task_routes={
    "app.workflows.scan.scan_task.run_scan_task": {"queue": "scan_queue"},
}