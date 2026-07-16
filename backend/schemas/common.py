"""
Shared Pydantic (v2) building blocks used across every resource's schemas.

Per skills.md > API Style, every list endpoint supports pagination, sorting,
and filtering -- `PaginatedResponse` is the common envelope for that.
"""
from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

ItemT = TypeVar("ItemT")


class ORMBaseModel(BaseModel):
    """
    Base for every "read" schema returned from the API.

    `from_attributes=True` lets these be built directly from SQLAlchemy ORM
    instances (`UserRead.model_validate(user_orm_instance)`) instead of
    manually unpacking each field in the router/service layer.
    """

    model_config = ConfigDict(from_attributes=True)


class GeoPoint(BaseModel):
    """
    A WGS84 (SRID 4326) coordinate pair.

    The API always speaks plain lat/lng JSON; the conversion to/from
    PostGIS's `geography(Point)` representation happens in the repository
    layer so no Pydantic schema needs to know about WKB/WKT encoding.
    """

    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class PaginatedResponse(BaseModel, Generic[ItemT]):
    """Standard pagination envelope for every `GET /api/v1/<resource>` list."""

    items: list[ItemT]
    total: int = Field(..., description="Total number of matching records, ignoring pagination.")
    page: int = Field(..., ge=1)
    page_size: int = Field(..., ge=1, le=100)

    @property
    def total_pages(self) -> int:
        if self.page_size == 0:
            return 0
        return -(-self.total // self.page_size)  # ceil division
