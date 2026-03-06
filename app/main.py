
from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from app.services.db.models import Base
from app.models.dependencies import get_db, engine
from app.workflows.scan.scan_task import run_scan_task
from app.auth.signup import router as signupRouter
from app.auth.login import router as loginRouter
from app.api.v1.routes import api_router as v1_api_router
from app.api.v2.routes import api_router as v2_api_router
from app.api.scan_image import api_router as scan_image_api_router
from app.api.report_generation import api_router as report_generation_api_router
from app.api.human_approval import api_router as human_approval_api_router
from app.api.scan_status import api_router as scan_status_api_router
from app.api.aduit_log import api_router as audit_log_api_router
from app.api.calibration_report import api_router as calibration_report_api_router
from app.business_rules.policy.relearn import api_router as relearn_policy_api_router
from app.api.submit_feedback import api_router as submit_feedback_api_router
from app.business_rules.policy.rollback import api_router as policy_rollback_api_router
from app.business_rules.policy.history import api_router as policy_history_api_router
from app.api.performance_analyzer import api_router as performance_analyzer_api_router
from app.business_rules.routing.optimize import api_router as optimize_routing_api_router
from app.api.admin_dashboard import api_router as admin_dashboard_api_router
from app.api.admin_health_check import api_router as admin_health_check_api_router
from app.api.admin_alerts import api_router as admin_alerts_api_router
from app.api.export_training_data import api_router as export_training_data_api_router
from app.services.scheduler.scheduler import start_scheduler

# prometheus-fastapi-instrumentator is optional; if not installed we skip instrumentation
try:
    from prometheus_fastapi_instrumentator import Instrumentator
except ImportError:
    Instrumentator = None


load_dotenv()

app = FastAPI(title="AI Image Scanner")
# enable Prometheus instrumentation only if library is available
if Instrumentator:
    Instrumentator().instrument(app).expose(app)
UPLOAD_DIR = "uploads"
REPORT_DIR = "reports"
REVIEW_THRESHOLD = 0.75

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

Base.metadata.create_all(bind=engine)
# ========== ROUTERS ==========
app.include_router(loginRouter)
app.include_router(signupRouter)
app.include_router(v1_api_router)
app.include_router(v2_api_router)
app.include_router(scan_image_api_router)
app.include_router(report_generation_api_router)
app.include_router(human_approval_api_router)
app.include_router(scan_status_api_router)
app.include_router(audit_log_api_router)
app.include_router(calibration_report_api_router)
app.include_router(relearn_policy_api_router)
app.include_router(submit_feedback_api_router)
app.include_router(policy_rollback_api_router)
app.include_router(policy_history_api_router)
app.include_router(performance_analyzer_api_router)
app.include_router(optimize_routing_api_router)
app.include_router(admin_dashboard_api_router)
app.include_router(admin_health_check_api_router)
app.include_router(admin_alerts_api_router)
app.include_router(export_training_data_api_router)

@app.on_event("startup")
def start_background_jobs():
    start_scheduler()
