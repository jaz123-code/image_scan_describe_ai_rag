# Models Documentation

## Overview

The `models/` folder contains all SQLAlchemy ORM models used throughout the AI Image Scanner application. This is the **single source of truth** for database models.

## Model Organization

### Core Models
- **`models.py`** - Base class and core `image` model
- **`user.py`** - User authentication model
- **`dependecies.py`** - Database session/engine configuration

### Scan & Results
- **`audit_log.py`** - Event audit trail (`AuditLog`)
- **`cost_calculate.py`** - Cost tracking (`CostHistory`) - **FIXED: Float type for costs**
- **`feedback.py`** - User feedback (`ScanFeedback`)
- **`evaluation.py`** - Field evaluation results (`Evaluation`)

### System Management
- **`system_policy.py`** - System policies (`SystemPolicy`, `SystemPolicy2`)
- **`system_alert.py`** - Health alerts (`SystemAlert`)
- **`rate_limit.py`** - Rate limiting (`RateLimit`)

### ML/Training
- **`model_registry.py`** - Model deployment tracking (`ModelRegistry`)
- **`training_dataset.py`** - Training dataset metadata (`TrainingDataset`)

### Legacy
- **`Policy.py`** - Legacy policy model (use `system_policy.py` instead)
- **`scan_result.py`** - Deprecated (empty)

## Important Imports

### Correct Way (Recommended)
```python
from app.models import (
    Base,
    image,
    User,
    AuditLog,
    ScanFeedback,
    Evaluation,
    SystemAlert,
    SystemPolicy2,
    CostHistory,
    TrainingDataset,
    ModelRegistry,
    RateLimit,
)
```

### Direct Imports (Also OK)
```python
from app.models.user import User
from app.models.audit_log import AuditLog
from app.models.cost_calculate import CostHistory
```

## Key Fixes Applied

### Bug Fixes
1. ✅ **audit_log.py** - Fixed typo: `create_at` → `created_at`
2. ✅ **cost_calculate.py** - Fixed type: `Integer` → `Float` for accurate cost calculations
3. ✅ **Added Float import** to cost_calculate.py

### Deduplication
- ✅ Removed duplicate models from `workflows/domain/`
- ✅ Updated `workflows/domain/__init__.py` to re-export from `app.models`
- ✅ Marked deprecated files with clear warnings

### Documentation
- ✅ Added comprehensive docstrings to all models
- ✅ Added module-level documentation
- ✅ Created `__init__.py` with proper exports

## Model Relationships

```
image (core)
├── CostHistory (foreign key)
├── AuditLog (indexed by image_id)
├── ScanFeedback (indexed by scan_id/user_id)
├── Evaluation (indexed by scan_id)
└── ModelRegistry (traffic distribution)

User
├── ScanFeedback (indexed by user_id)
└── AuditLog (indexed by scan_id)

SystemPolicy2 (versioned configuration)
```

## Database Session

All database operations should use the session from `models/dependecies.py`:

```python
from app.models.dependecies import get_db, SessionLocal

# In FastAPI endpoints
async def my_endpoint(db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == 1).first()
```

## Adding New Models

1. Create a new file in `models/` (e.g., `new_model.py`)
2. Import `Base` from `models.py`
3. Define your model class inheriting from `Base`
4. Add to `models/__init__.py` exports
5. Add docstring documentation

Example:
```python
from sqlalchemy import Column, Integer, String
from app.models.models import Base

class NewModel(Base):
    """Documentation for the model."""
    __tablename__ = "new_model"
    id = Column(Integer, primary_key=True)
    name = Column(String)
```

## Workflow Integration

Models in workflows should import from `app.models`, NOT from `workflows/domain/`:

```python
# ✅ CORRECT
from app.models import ModelRegistry, TrainingDataset

# ❌ INCORRECT
from app.workflows.domain import ModelRegistry
```
