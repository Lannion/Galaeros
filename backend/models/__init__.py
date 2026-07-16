# backend/app/models/__init__.py
"""
Domain models package.

Every model must be imported here so SQLAlchemy's mapper registry can
resolve the string-based relationship() targets used across these files
(e.g. Stop.route_links -> "RouteStop"). Importing app.models is enough to
register the full model graph — individual modules deliberately avoid
importing each other directly to sidestep circular imports.
"""

from .base import Base
from .enums import ContributorRank, RouteStatus, StopType, UserRole, VehicleType
from .route import Route
from .route_stop import RouteStop
from .stop import Stop
from .user import User

__all__ = [
    "Base",
    "User",
    "Stop",
    "Route",
    "RouteStop",
    "UserRole",
    "ContributorRank",
    "VehicleType",
    "RouteStatus",
    "StopType",
]