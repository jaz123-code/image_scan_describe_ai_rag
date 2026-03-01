"""
Models Structure and Dependencies Overview

This file documents the relationships and organization of all SQLAlchemy models
in the application for reference and architectural understanding.
"""

"""
CORE MODELS HIERARCHY
=====================

Base (declarative_base)
├── image
│   ├── Primary: image_id (str)
│   ├── user_id (str, foreign key to User.id)
│   └── image_content (str, JSON)
│
├── User  
│   ├── Primary: id (int)
│   ├── email (str, unique)
│   └── hashed_password (str)
│
├── AuditLog
│   ├── Primary: id (str)
│   ├── scan_id (str, FK to image.image_id)
│   ├── event_type (str)
│   ├── message (text)
│   └── created_at (datetime)
│
├── ScanFeedback
│   ├── Primary: id (str)
│   ├── scan_id (str, FK to image.image_id)
│   ├── user_id (str, FK to User.id)
│   ├── original_output (text, JSON)
│   ├── corrected_output (text, JSON)
│   └── created_at (datetime)
│
├── Evaluation
│   ├── Primary: id (str)
│   ├── scan_id (str, FK to image.image_id)
│   ├── field (str)
│   ├── result (str: CORRECT|INCORRECT|PARTIAL)
│   └── (no created_at)
│
├── CostHistory  ** FIXED: cost column is Float **
│   ├── Primary: id (int)
│   ├── image_id (str, FK to image.image_id)
│   ├── cost (float) ✅ FIXED from Integer
│   └── currency (str)
│
├── SystemAlert
│   ├── Primary: id (int)
│   ├── type (str: HIGH_COST, LOW_ACCURACY, etc)
│   ├── message (str)
│   ├── severity (str: INFO|WARNING|CRITICAL)
│   └── created_at (datetime)
│
├── SystemPolicy (Legacy)
│   ├── Primary: key (str)
│   ├── value (str)
│   └── updated_at (datetime)
│
├── SystemPolicy2 (Current)
│   ├── Primary: id (int)
│   ├── key (str, indexed)
│   ├── value (str)
│   ├── version (int)
│   ├── is_active (bool)
│   └── created_at (datetime)
│
├── ModelRegistry
│   ├── Primary: id (int)
│   ├── model_name (str)
│   ├── version (int)
│   ├── accuracy (float)
│   ├── traffic_percentage (float)
│   ├── is_active (bool)
│   └── created_at (datetime)
│
├── TrainingDataset
│   ├── Primary: id (int)
│   ├── file_path (str)
│   ├── record_count (int)
│   └── created_at (datetime)
│
├── RateLimit
│   ├── Primary: key (str, IP address)
│   ├── count (int)
│   └── window_start (datetime)
│
└── system_policy (Legacy - duplicate of SystemPolicy)
    ├── Primary: key (str)
    ├── value (str)
    └── updated_at (datetime)


CRITICAL RELATIONSHIPS
======================

1. PRIMARY DATA FLOW
   User → image → (AuditLog, CostHistory, ScanFeedback, Evaluation)
   
2. FEEDBACK & LEARNING LOOP
   ScanFeedback → TrainingDataset → ModelRegistry
   
3. SYSTEM MANAGEMENT
   SystemPolicy2 (configuration) ← (SystemAlert, RateLimit)
   
4. MODEL DEPLOYMENT
   ModelRegistry (with canary traffic splitting)


DATABASE SESSION INJECTION
==========================

All FastAPI endpoints should use:
    from app.models.dependencies import get_db
    
    async def endpoint(db: Session = Depends(get_db)):
        user = db.query(User).filter(User.id == 1).first()
        db.add(new_record)
        db.commit()


IMPORT PATTERNS
===============

✅ CORRECT:
    from app.models import User, CostHistory, ModelRegistry
    from app.models.user import User
    from app.models.dependencies import get_db, SessionLocal

❌ INCORRECT:
    from app.workflows.domain.model_registry import ModelRegistry
    from app.models.model_registry import ModelRegistry as DuplicateModel


RECENT FIXES
============

1. audit_log.py
   - Fixed: create_at → created_at
   
2. cost_calculate.py  
   - Fixed: cost column type Integer → Float
   - Added: Float to imports
   
3. Deduplication
   - Removed duplicate ModelRegistry from workflows/domain/
   - Removed duplicate TrainingDataset from workflows/domain/
   - Marked as DEPRECATED with clear warnings
   
4. Documentation
   - Added comprehensive docstrings to all models
   - Created models/__init__.py with proper exports
   - Created models/README.md with full documentation


TODO / IMPROVEMENTS
===================

[ ] Future: Add updated_at timestamp to all models
[ ] Future: Add soft delete (is_deleted flag) patterns
[ ] Future: Add database constraint validation
[ ] Future: Add index optimization for frequently queried columns
[ ] Future: Add created_at index for time-series queries
"""

print(__doc__)
