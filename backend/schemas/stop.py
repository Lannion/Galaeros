"""Pydantic schemas for the `Stop` resource."""
from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from backend.models.enums import VehicleType
from backend.schemas.common import GeoPoint, ORMBaseModel


class StopCreate(BaseModel):
    """
    Payload for a community-submitted stop.

    `created_by_id` is not part of this schema -- the router derives it
    from the authenticated request, never from client input, so a user
    can't submit a contribution under someone else's name.
    """

    name: str = Field(..., min_length=1, max_length=150)
    description: str | None = Field(default=None, max_length=2000)
    location: GeoPoint
    address: str | None = Field(default=None, max_length=300)
    vehicle_types: list[VehicleType] = Field(..., min_length=1)
    barangay_id: uuid.UUID | None = None


class StopUpdate(BaseModel):
    """Partial update payload (PATCH semantics)."""

    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, max_length=2000)
    location: GeoPoint | None = None
    address: str | None = Field(default=None, max_length=300)
    vehicle_types: list[VehicleType] | None = Field(default=None, min_length=1)


class StopRead(ORMBaseModel):
    """A stop as returned by the API."""

    id: uuid.UUID
    name: str
    description: str | None
    location: GeoPoint
    address: str | None
    vehicle_types: list[VehicleType]
    barangay_id: uuid.UUID | None
    is_verified: bool
    created_by_id: uuid.UUID
    created_at: datetime

    # NOTE: `Stop.location` is a PostGIS `Geography` value on the ORM side
    # (a WKBElement), not a lat/lng-shaped attribute, so plain
    # `StopRead.model_validate(stop_orm_instance)` can't populate `location`
    # automatically. The repository layer decodes it (e.g. with
    # `geoalchemy2.shape.to_shape`) into a `GeoPoint` before handing data to
    # this schema -- typically by building the dict explicitly rather than
    # validating the ORM object directly, for this field only.
