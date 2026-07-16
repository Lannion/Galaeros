"""`Route` repository -- raw persistence queries against `routes` and
`route_stops`."""
from __future__ import annotations

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models.enums import RouteStatus, VehicleType
from backend.models.route import Route
from backend.models.route_stop import RouteStop
from backend.schemas.route import RouteStopInput

_WITH_STOPS = selectinload(Route.stop_links).selectinload(RouteStop.stop)


async def get_by_id(db: AsyncSession, *, route_id: uuid.UUID) -> Route | None:
    result = await db.execute(
        select(Route)
        .where(Route.id == route_id, Route.deleted_at.is_(None))
        .options(_WITH_STOPS)
    )
    return result.scalar_one_or_none()


async def create(
    db: AsyncSession,
    *,
    name: str,
    description: str | None,
    vehicle_type: VehicleType,
    base_fare: float | None,
    stops: list[RouteStopInput],
    path=None,
) -> Route:
    route = Route(
        name=name,
        description=description,
        vehicle_type=vehicle_type,
        base_fare=base_fare,
        path=path,
        # `status` isn't set here -- it defaults to RouteStatus.PENDING at
        # the database level (see Route.status's `default=`/`server_default`).
    )
    route.stop_links = [
        RouteStop(
            stop_id=stop_input.stop_id,
            sequence=position,
            fare_to_next_stop=stop_input.fare_to_next_stop,
            distance_meters_to_next_stop=stop_input.distance_meters_to_next_stop,
        )
        for position, stop_input in enumerate(stops)
    ]
    db.add(route)
    await db.flush()
    await db.refresh(route)
    return await get_by_id(db, route_id=route.id)  # re-fetch with stops eager-loaded


async def save(db: AsyncSession, *, route: Route) -> Route:
    await db.flush()
    await db.refresh(route)
    return route


async def list_routes(
    db: AsyncSession,
    *,
    offset: int,
    limit: int,
    vehicle_type: VehicleType | None = None,
    status: RouteStatus | None = None,
    search: str | None = None,
) -> tuple[list[Route], int]:
    query = select(Route).where(Route.deleted_at.is_(None)).options(_WITH_STOPS)
    count_query = select(func.count()).select_from(Route).where(Route.deleted_at.is_(None))

    if vehicle_type is not None:
        query = query.where(Route.vehicle_type == vehicle_type)
        count_query = count_query.where(Route.vehicle_type == vehicle_type)

    if status is not None:
        query = query.where(Route.status == status)
        count_query = count_query.where(Route.status == status)

    if search:
        pattern = f"%{search}%"
        query = query.where(Route.name.ilike(pattern))
        count_query = count_query.where(Route.name.ilike(pattern))

    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    result = await db.execute(query.order_by(Route.name).offset(offset).limit(limit))
    return list(result.scalars().all()), total