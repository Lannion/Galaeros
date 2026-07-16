"""`Stop` repository -- raw persistence queries against the `stops` table,
including the PostGIS-backed "stops near me" search.

`Stop.location` is `Geometry(POINT, srid=4326)`, not `Geography`. For a
geometry column, PostGIS treats `ST_DWithin`'s radius argument in the
column's own SRID units -- for SRID 4326 that's *degrees*, not meters. Both
sides are cast to `geography` below specifically so `radius_meters` means
what it says; the cast is cheap since the underlying coordinates don't
change, only how PostGIS interprets distance between them (spheroidal
instead of planar).
"""
from __future__ import annotations

import uuid

from geoalchemy2 import Geography
from geoalchemy2.functions import ST_DWithin, ST_MakePoint, ST_SetSRID
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import Point
from sqlalchemy import cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.enums import StopType
from backend.models.stop import Stop
from backend.schemas.common import GeoPoint


def to_geo_point(stop: Stop) -> GeoPoint:
    """Decode a `Stop.location` PostGIS value into a plain `GeoPoint` DTO."""
    point: Point = to_shape(stop.location)
    return GeoPoint(latitude=point.y, longitude=point.x)


def make_location(point: GeoPoint):
    """Encode a `GeoPoint` DTO into the WKBElement PostGIS expects on write."""
    return from_shape(Point(point.longitude, point.latitude), srid=4326)


async def get_by_id(db: AsyncSession, *, stop_id: uuid.UUID) -> Stop | None:
    result = await db.execute(
        select(Stop).where(Stop.id == stop_id, Stop.deleted_at.is_(None))
    )
    return result.scalar_one_or_none()


async def create(
    db: AsyncSession,
    *,
    name: str,
    stop_type: StopType,
    location: GeoPoint,
    city: str | None,
    barangay: str | None,
) -> Stop:
    stop = Stop(
        name=name,
        stop_type=stop_type,
        location=make_location(location),
        city=city,
        barangay=barangay,
    )
    db.add(stop)
    await db.flush()
    await db.refresh(stop)
    return stop


async def save(db: AsyncSession, *, stop: Stop) -> Stop:
    await db.flush()
    await db.refresh(stop)
    return stop


async def list_stops(
    db: AsyncSession,
    *,
    offset: int,
    limit: int,
    stop_type: StopType | None = None,
    city: str | None = None,
    barangay: str | None = None,
    near: tuple[GeoPoint, int] | None = None,
) -> tuple[list[Stop], int]:
    """
    List stops with optional filters.

    `near` is `(center, radius_meters)`; when given, results are restricted
    to stops within that radius via `ST_DWithin` on `Stop.location` cast to
    `geography`, using the GIST index already on that column
    (`idx_stops_location`) to stay fast at scale.
    """
    query = select(Stop).where(Stop.deleted_at.is_(None))
    count_query = select(func.count()).select_from(Stop).where(Stop.deleted_at.is_(None))

    if stop_type is not None:
        query = query.where(Stop.stop_type == stop_type)
        count_query = count_query.where(Stop.stop_type == stop_type)

    if city is not None:
        query = query.where(Stop.city == city)
        count_query = count_query.where(Stop.city == city)

    if barangay is not None:
        query = query.where(Stop.barangay == barangay)
        count_query = count_query.where(Stop.barangay == barangay)

    if near is not None:
        center, radius_meters = near
        center_point = cast(ST_SetSRID(ST_MakePoint(center.longitude, center.latitude), 4326), Geography)
        within = ST_DWithin(cast(Stop.location, Geography), center_point, radius_meters)
        query = query.where(within)
        count_query = count_query.where(within)

    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    result = await db.execute(query.order_by(Stop.name).offset(offset).limit(limit))
    return list(result.scalars().all()), total
