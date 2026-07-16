"""
Aggregates every `v1/endpoints/*` router into a single `api_router`.

`main.py` mounts this once:

    from backend.api.v1.api import api_router
    app.include_router(api_router, prefix="/api/v1")
"""
from fastapi import APIRouter

from backend.api.v1.endpoints import routes, stops, users

api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(stops.router)
api_router.include_router(routes.router)
