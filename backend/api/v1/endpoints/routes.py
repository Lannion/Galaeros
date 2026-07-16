"""`/api/v1/routes` -- transportation route discovery and community
contributions."""
from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from geoalchemy2.shape import to_shape
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.deps import PaginationParams, get_current_active_user, get_db
from backend.models.enums import RouteStatus, VehicleType
from backend.models.route import Route
from backend.models.stop import Stop
from backend.models.user import User
from backend.repositories.stop_repository import to_geo_point
from backend.schemas.common import GeoPoint, PaginatedResponse
from backend.schemas.route import RouteCreate, RouteRead, RouteStopRead, RouteUpdate
from backend.schemas.stop import StopRead
from backend.services import route_service
from backend.services.route_service import InvalidStopReferenceError

router = APIRouter(prefix="/routes", tags=["routes"])


def _to_stop_read(stop: Stop) -> StopRead:
    return StopRead(
        id=stop.id,
        name=stop.name,
        stop_type=stop.stop_type,
        location=to_geo_point(stop),
        city=stop.city,
        barangay=stop.barangay,
    )


def _to_route_read(route: Route) -> RouteRead:
    """
    Build a `RouteRead` from a `Route` ORM instance.

    Both `Route.path` and each linked `Stop.location` are PostGIS values,
    not plain-attribute-shaped, so this decodes them explicitly rather than
    relying on `model_validate`.
    """
    path = None
    if route.path is not None:
        line = to_shape(route.path)
        path = [GeoPoint(latitude=lat, longitude=lng) for lng, lat in line.coords]

    return RouteRead(
        id=route.id,
        name=route.name,
        description=route.description,
        vehicle_type=route.vehicle_type,
        status=route.status,
        base_fare=route.base_fare,
        stops=[
            RouteStopRead(
                sequence=link.sequence,
                fare_to_next_stop=link.fare_to_next_stop,
                distance_meters_to_next_stop=link.distance_meters_to_next_stop,
                stop=_to_stop_read(link.stop),
            )
            for link in route.stop_links
        ],
        path=path,
    )


@router.post("", response_model=RouteRead, status_code=status.HTTP_201_CREATED)
async def create_route(
    payload: RouteCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> RouteRead:
    try:
        route = await route_service.create_route(db, data=payload, created_by=current_user)
    except InvalidStopReferenceError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    return _to_route_read(route)


@router.get("", response_model=PaginatedResponse[RouteRead])
async def list_routes(
    pagination: PaginationParams = Depends(),
    vehicle_type: VehicleType | None = Query(default=None),
    route_status: RouteStatus | None = Query(default=None, alias="status"),
    search: str | None = Query(default=None, max_length=160),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[RouteRead]:
    routes, total = await route_service.list_routes(
        db,
        offset=pagination.offset,
        limit=pagination.page_size,
        vehicle_type=vehicle_type,
        status=route_status,
        search=search,
    )
    return PaginatedResponse(
        items=[_to_route_read(r) for r in routes],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/{route_id}", response_model=RouteRead)
async def read_route(route_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> RouteRead:
    route = await route_service.get_by_id(db, route_id=route_id)
    if route is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found.")
    return _to_route_read(route)


@router.patch("/{route_id}", response_model=RouteRead)
async def update_route(
    route_id: uuid.UUID,
    payload: RouteUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> RouteRead:
    route = await route_service.get_by_id(db, route_id=route_id)
    if route is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found.")

    if not await route_service.can_edit(db, route=route, user=current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the original contributor or a moderator can edit this route.",
        )

    updated = await route_service.update_route(db, route=route, payload=payload)
    return _to_route_read(updated)
