"""`/api/v1/stops` -- transit stop discovery and community contributions."""
from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.deps import PaginationParams, get_current_active_user, get_db
from backend.models.enums import StopType
from backend.models.user import User
from backend.repositories.stop_repository import to_geo_point
from backend.schemas.common import PaginatedResponse
from backend.schemas.stop import StopCreate, StopRead, StopUpdate
from backend.services import stop_service

router = APIRouter(prefix="/stops", tags=["stops"])


def _to_stop_read(stop) -> StopRead:  # type: ignore[no-untyped-def]
    """
    Build a `StopRead` from a `Stop` ORM instance.

    `Stop.location` is a PostGIS geometry value, not a `GeoPoint`-shaped
    attribute, so it can't come from plain `model_validate`; it's decoded
    explicitly here and merged with the rest of the ORM object's fields.
    """
    return StopRead(
        id=stop.id,
        name=stop.name,
        stop_type=stop.stop_type,
        location=to_geo_point(stop),
        city=stop.city,
        barangay=stop.barangay,
    )


@router.post("", response_model=StopRead, status_code=status.HTTP_201_CREATED)
async def create_stop(
    payload: StopCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> StopRead:
    stop = await stop_service.create_stop(db, data=payload, created_by=current_user)
    return _to_stop_read(stop)


@router.get("", response_model=PaginatedResponse[StopRead])
async def list_stops(
    pagination: PaginationParams = Depends(),
    stop_type: StopType | None = Query(default=None),
    city: str | None = Query(default=None, max_length=100),
    barangay: str | None = Query(default=None, max_length=100),
    near_latitude: float | None = Query(default=None, ge=-90, le=90),
    near_longitude: float | None = Query(default=None, ge=-180, le=180),
    radius_meters: int | None = Query(default=None, ge=1, le=50_000),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[StopRead]:
    stops, total = await stop_service.list_stops(
        db,
        offset=pagination.offset,
        limit=pagination.page_size,
        stop_type=stop_type,
        city=city,
        barangay=barangay,
        near_latitude=near_latitude,
        near_longitude=near_longitude,
        radius_meters=radius_meters,
    )
    return PaginatedResponse(
        items=[_to_stop_read(s) for s in stops],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get("/{stop_id}", response_model=StopRead)
async def read_stop(stop_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> StopRead:
    stop = await stop_service.get_by_id(db, stop_id=stop_id)
    if stop is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stop not found.")
    return _to_stop_read(stop)


@router.patch("/{stop_id}", response_model=StopRead)
async def update_stop(
    stop_id: uuid.UUID,
    payload: StopUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> StopRead:
    stop = await stop_service.get_by_id(db, stop_id=stop_id)
    if stop is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stop not found.")

    if not await stop_service.can_edit(db, stop=stop, user=current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the original contributor or a moderator can edit this stop.",
        )

    updated = await stop_service.update_stop(db, stop=stop, payload=payload)
    return _to_stop_read(updated)
