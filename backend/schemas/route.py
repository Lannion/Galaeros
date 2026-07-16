"""
Pydantic schemas for the `Route` resource.

Matches `backend.models.route.Route` + `backend.models.route_stop.RouteStop`:
no `code`, `is_verified`, or `created_by_id` fields exist on `Route`
(unlike an earlier draft of this schema) -- it has `status: RouteStatus`
and a `path` geometry instead. Attribution lives on `Contribution`, same as
`Stop`. `RouteStop`'s real per-leg fields are `fare_to_next_stop` /
`distance_meters_to_next_stop`, not `leg_duration_seconds`.
"""
from __future__ import annotations

import uuid

from pydantic import BaseModel, Field

from backend.models.enums import RouteStatus, VehicleType
from backend.schemas.common import GeoPoint
from backend.schemas.stop import StopRead


class RouteStopInput(BaseModel):
    """
    One stop within a route-creation payload, in board order.

    `sequence` isn't part of this schema -- the service assigns it from
    list position, so a client can't submit gaps/duplicates. The fare and
    distance describe the leg from *this* stop to the *next* one in the
    list (meaningless on the last stop, so leave both null there).
    """

    stop_id: uuid.UUID
    fare_to_next_stop: float | None = Field(default=None, ge=0)
    distance_meters_to_next_stop: int | None = Field(default=None, ge=0)


class RouteCreate(BaseModel):
    """Payload for a community-submitted route."""

    name: str = Field(..., min_length=1, max_length=160)
    description: str | None = Field(default=None, max_length=500)
    vehicle_type: VehicleType
    base_fare: float | None = Field(default=None, ge=0)
    stops: list[RouteStopInput] = Field(
        ..., min_length=2, description="At least an origin and a destination, in board order."
    )


class RouteUpdate(BaseModel):
    """
    Partial update payload (PATCH semantics) for route metadata only.

    Doesn't cover `stops`/`path` (re-sequencing is a bigger operation, see
    `route_service.update_route`) or `status` (a moderation decision, not a
    general edit).
    """

    name: str | None = Field(default=None, min_length=1, max_length=160)
    description: str | None = Field(default=None, max_length=500)
    base_fare: float | None = Field(default=None, ge=0)


class RouteStopRead(BaseModel):
    """
    One stop's position within a route, as returned by the API.

    Built explicitly by the router rather than via `model_validate` --
    `stop` needs `StopRead`'s own manual construction to decode
    `Stop.location` (see `api.v1.endpoints.routes._to_route_read`).
    """

    sequence: int
    fare_to_next_stop: float | None
    distance_meters_to_next_stop: int | None
    stop: StopRead


class RouteRead(BaseModel):
    """
    A route as returned by the API, with its full ordered stop list.

    Built explicitly by the router, not `model_validate`d directly from the
    ORM object: both `stops[].stop.location` and `path` are PostGIS values
    that need explicit decoding first.
    """

    id: uuid.UUID
    name: str
    description: str | None
    vehicle_type: VehicleType
    status: RouteStatus
    base_fare: float | None
    stops: list[RouteStopRead]
    path: list[GeoPoint] | None = None


class RouteSummary(BaseModel):
    """Lightweight route shape for search result lists, without the full stop list."""

    id: uuid.UUID
    name: str
    vehicle_type: VehicleType
    status: RouteStatus
    base_fare: float | None
