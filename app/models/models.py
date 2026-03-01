"""
Compatibility shim for legacy model imports.

Exposes `Base` from the centralized DB models module so older
imports like `from app.models.models import Base` continue to work.
"""

from app.services.db.models import Base

__all__ = ["Base"]
