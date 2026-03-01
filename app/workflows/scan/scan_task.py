import json
import uuid
from sqlalchemy.orm import Session

from app.utils.custom_json_encoder import CustomJSONEncoder
from app.utils.utils import parse_vision_response
from app.utils.schema_guard import enforce_schema

from app.services.confidence import calculate_confidence
from app.services.validator import validate_scan
from app.services.audit_logger import log_event
from app.services.progress_updater import update_progress
from app.services.calculate_cost import calculate_cost
from app.business_rules.routing.model_router import run_with_routing
from app.services.calibration_lookup import calibration_lookup

from app.services.db.models import image as ImageModel
from app.models.cost_calculate import CostHistory
from app.services.active_learning import should_request_human_review
from app.infrastructure.celery_app import celery_app
from app.models.dependencies import SessionLocal

REVIEW_THRESHOLD = 0.75
MAX_COST_LIMIT = 1000.0


@celery_app.task(name="app.workflows.scan.scan_task.run_scan_task", bind=True,autoretry_for=(Exception,),retry_backoff=True, retry_backoff_max=600,retry_jitter=True, retry_kwargs={"max_retries": 5})
def run_scan_task(
    self,
    image_id: str,
    image_path: str,
    provider: str,
    auto_threshold: float,
):
    db = SessionLocal()
    try:
        print("🚀 Celery task started!")
        print(f"Image ID: {image_id}")
        print(f"Provider: {provider}")
        # -----------------------------------
        # COST INITIALIZATION
        # -----------------------------------
        cost_record = (
            db.query(CostHistory)
            .filter(CostHistory.image_id == image_id)
            .first()
        )
        print(f"proccessing: {image_id}")

        if not cost_record:
            cost_record = CostHistory(
                id=str(uuid.uuid4()),
                image_id=image_id,
                cost=0.0,
                currency="USD"
            )
            db.add(cost_record)
            db.commit()

        if cost_record.cost >= MAX_COST_LIMIT:
            raise ValueError("Cost limit exceeded, recharge required")

        # -----------------------------------
        # PROGRESS: START
        # -----------------------------------
        update_progress(db, image_id, progress=0, stage="STARTED",
                        message="Scan task started")

        update_progress(db, image_id, progress=20, stage="IMAGE_PREPROCESSING",
                        message="Image loaded successfully")

        # -----------------------------------
        # MODEL ROUTING
        # -----------------------------------
        routing_output = run_with_routing(image_path, calibration_lookup)

        update_progress(db, image_id, progress=40, stage="MODEL_ANALYSIS",
                        message="Vision model analyzing image")

        vision_result = routing_output["result"]
        escalated = routing_output.get("escalated", False)

        # vision_result is the dict returned by engine.analyze
        # We need to extract the raw response string for parsing
        raw_response = vision_result.get("raw_response", "{}")
        
        parsed = enforce_schema(parse_vision_response(raw_response))

        # -----------------------------------
        # COST CALCULATION
        # -----------------------------------
        model_metadata = vision_result.get("model_metadata", {})
        provider_name = model_metadata.get("provider", "unknown")
        model_name = model_metadata.get("model", "unknown")

        scan_cost = calculate_cost(provider_name, model_name)
        cost_record.cost += scan_cost
        db.commit()

        # -----------------------------------
        # CONFIDENCE SCORING
        # -----------------------------------
        update_progress(db, image_id, progress=65, stage="CONFIDENCE_SCORING",
                        message="Calculating confidence scores")

        extracted_data = parsed.get("extracted_data", {})
        fields, overall_confidence = calculate_confidence(extracted_data)

        # -----------------------------------
        # VALIDATION
        # -----------------------------------
        update_progress(db, image_id, progress=80, stage="VALIDATION",
                        message="Validating extracted fields")

        warnings = validate_scan(fields)

        status = (
            "AUTO_APPROVED"
            if overall_confidence >= auto_threshold
            else "PENDING_REVIEW"
        )

        log_event(
            db,
            image_id,
            "SCAN_COMPLETED",
            f"Status={status}, confidence={overall_confidence}, escalated={escalated}"
        )

        # -----------------------------------
        # FINAL RESULT
        # -----------------------------------
        scan_result = {
            "document_type": parsed.get("document_type", "N/A"),
            "confidence": overall_confidence,
            "fields": fields,
            "status": status,
            "summary": parsed.get("summary", ""),
            "warnings": warnings,
            "progress": 100,
            "stage": "COMPLETED",
            "routing": {
                "escalated": escalated,
                "provider": provider_name,
                "model": model_name
            },
            "security_checks": {
                "file_validated": True,
                "schema_validated": True,
                "model_validated": True
            },
            "cost": {
                "currency": "USD",
                "amount": scan_cost,
                "provider": provider_name,
                "model": model_name
            }
        }
        review_decision=should_request_human_review(scan_result)
        if review_decision["request_review"]:
            scan_result["status"]="PENDING_REVIEW"
        else:
            scan_result["status"]="AUTO_APPROVED"
        scan_result["active_learning"]=review_decision
        log_event(
            db,
            image_id,
            "ACTIVE_LEARNING_DECISION",
            f"review={review_decision['request_review']} reasons={review_decision['reasons']}"
        )
        log_event(
            db,
            image_id,
            "SCAN_COMPLETED",
            f"Status={scan_result['status']}, confidence={overall_confidence}, escalated={escalated}"
        )
          # -----------------------------------
    # PERSIST RESULT
    #----------------------------------- 
        record = (
                db.query(ImageModel)
                .filter(ImageModel.image_id == image_id)
                .first()
                )
        if record:
            record.image_content = json.dumps(scan_result, cls=CustomJSONEncoder)
            db.commit()

    except Exception as e:
        log_event(db, image_id, "SCAN_FAILED", str(e))
        raise self.retry(exc=e, countdown=5)

    finally:
        db.close()
