"""`Route` service -- business logic between the API routers and the route
repository: stop-existence validation, deriving `path` from the ordered
stop sequence, and edit authorization.

`Route` itself has no `created_by_id` -- attribution is tracked via a
`Contribution` row created alongside every new `Route`, the same pattern
`stop_service` uses (see `models/contribution.py`).
"""
from __future__ import annotations

import uuid

from geoalchemy2.shape import from_shape
from shapely.geometry import LineString
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.enums import ContributionTargetType, RouteStatus, UserRole, VehicleType
from backend.models.route import Route
from backend.models.user import User
from backend.repositories import contribution_repository, route_repository, stop_repository
from backend.schemas.route import RouteCreate, RouteUpdate


class InvalidStopReferenceError(ValueError):
    """Raised when a route references a stop_id that doesn't exist."""


async def get_by_id(db: AsyncSession, *, route_id: uuid.UUID) -> Route | None:
    return await route_repository.get_by_id(db, route_id=route_id)


async def create_route(db: AsyncSession, *, data: RouteCreate, created_by: User) -> Route:
    # Validate every referenced stop exists (fails with a clear 4xx instead
    # of a DB FK violation surfacing as a 500), and collect each one's
    # location so `path` can be derived from the same ordered sequence that
    # defines the route -- see route.py's docstring: "`path` is a
    # rendering/distance convenience derived from that sequence, not the
    # source of truth."
    points = []
    for stop_input in data.stops:
        stop = await stop_repository.get_by_id(db, stop_id=stop_input.stop_id)
        if stop is None:
            raise InvalidStopReferenceError(f"Stop {stop_input.stop_id} does not exist.")
        points.append(stop_repository.to_geo_point(stop))

    path = None
    if len(points) >= 2:
        path = from_shape(
            LineString([(p.longitude, p.latitude) for p in points]),
            srid=4326,
        )

    route = await route_repository.create(
        db,
        name=data.name,
        description=data.description,
        vehicle_type=data.vehicle_type,
        base_fare=data.base_fare,
        stops=data.stops,
        path=path,
    )

    # Record who submitted it. This starts the route at RouteStatus.PENDING
    # (the model's default); a moderator promoting it to ACTIVE is what
    # "verification" means here -- see ARCHITECTURE.md > Community
    # Verification.
    await contribution_repository.create(
        db,
        target_type=ContributionTargetType.ROUTE,
        route_id=route.id,
        submitted_by_id=created_by.id,
    )
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
    return await route_repository.list_routes(
        db, offset=offset, limit=limit, vehicle_type=vehicle_type, status=status, search=search
    )


async def can_edit(db: AsyncSession, *, route: Route, user: User) -> bool:
    """
    Only the original submitter or a moderator+ may edit a route.

    Queries `Contribution` for the answer since `Route` doesn't store who
    created it -- same reasoning as `stop_service.can_edit`.
    """
    if user.role in (UserRole.MODERATOR, UserRole.ADMINISTRATOR):
        return True

    submitter_id = await contribution_repository.get_original_submitter_id(
        db, target_type=ContributionTargetType.ROUTE, target_id=route.id
    )
    return submitter_id == user.id


async def update_route(db: AsyncSession, *, route: Route, payload: RouteUpdate) -> Route:
    """
    Apply a partial update to route metadata only.

    Doesn't touch `stop_links` or `path`: re-sequencing a route's stops is
    a bigger operation (it would need to rebuild `path` too, and could
    orphan `RouteStop` rows) -- left as a separate endpoint/service
    function rather than folded into a generic PATCH. Also doesn't touch
    `status`, which is a moderation decision, not a general edit.
    """
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(route, field, value)
    return await route_repository.save(db, route=route)
