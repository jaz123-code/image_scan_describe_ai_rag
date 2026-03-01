"""
Workflow Domain Models (Re-exports from app.models)

Note: This folder contains domain models used in workflows.
All models are defined and maintained in app.models/ to maintain a single source of truth.

Import models from:
- from app.models import ModelRegistry, TrainingDataset
"""

# Re-export models for convenience in workflow modules
from app.models import ModelRegistry, TrainingDataset

__all__ = [
    "ModelRegistry",
    "TrainingDataset",
]
