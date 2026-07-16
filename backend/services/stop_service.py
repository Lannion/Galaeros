"""`Stop` service -- business logic between the API routers and the stop
repository, including who's allowed to edit a given stop.

`Stop` itself has no `created_by_id` -- attribution is tracked via a
`Contribution` row created alongside every new `Stop` (see
`models/contribution.py`).
"""
from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.enums import ContributionTargetType, StopType, UserRole
from backend.models.stop import Stop
from backend.models.user import User
from backend.repositories import contribution_repository, stop_repository
from backend.schemas.common import GeoPoint
from backend.schemas.stop import StopCreate, StopUpdate


async def get_by_id(db: AsyncSession, *, stop_id: uuid.UUID) -> Stop | None:
    return await stop_repository.get_by_id(db, stop_id=stop_id)


async def create_stop(db: AsyncSession, *, data: StopCreate, created_by: User) -> Stop:
    stop = await stop_repository.create(
        db,
        name=data.name,
        stop_type=data.stop_type,
        location=data.location,
        city=data.city,
        barangay=data.barangay,
    )
    # Record who submitted it. This Contribution starts PENDING; a
    # moderator flipping its status is what "verification" means here --
    # see ARCHITECTURE.md > Community Verification.
    await contribution_repository.create(
        db,
        target_type=ContributionTargetType.STOP,
        stop_id=stop.id,
        submitted_by_id=created_by.id,
    )
    return stop


async def list_stops(
    db: AsyncSession,
    *,
    offset: int,
    limit: int,
    stop_type: StopType | None = None,
    city: str | None = None,
    barangay: str | None = None,
    near_latitude: float | None = None,
    near_longitude: float | None = None,
    radius_meters: int | None = None,
) -> tuple[list[Stop], int]:
    near = None
    if near_latitude is not None and near_longitude is not None:
        near = (
            GeoPoint(latitude=near_latitude, longitude=near_longitude),
            radius_meters or 1000,
        )
    return await stop_repository.list_stops(
        db,
        offset=offset,
        limit=limit,
        stop_type=stop_type,
        city=city,
        barangay=barangay,
        near=near,
    )


async def can_edit(db: AsyncSession, *, stop: Stop, user: User) -> bool:
    """
    Only the original submitter or a moderator+ may edit a stop.

    Unlike a simple `stop.created_by_id == user.id` check, this has to
    query `Contribution` for the answer, since `Stop` doesn't store who
    created it.
    """
    if user.role in (UserRole.MODERATOR, UserRole.ADMINISTRATOR):
        return True

    submitter_id = await contribution_repository.get_original_submitter_id(
        db, target_type=ContributionTargetType.STOP, target_id=stop.id
    )
    return submitter_id == user.id


async def update_stop(db: AsyncSession, *, stop: Stop, payload: StopUpdate) -> Stop:
    update_data = payload.model_dump(exclude_unset=True)

    if "location" in update_data:
        location: GeoPoint = update_data.pop("location")
        stop.location = stop_repository.make_location(location)

    for field, value in update_data.items():
        setattr(stop, field, value)

    return await stop_repository.save(db, stop=stop)
