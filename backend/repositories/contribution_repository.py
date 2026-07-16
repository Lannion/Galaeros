"""`Contribution` repository -- raw persistence queries against the
`contributions` table. See `models/contribution.py` for why this exists
separately from `Stop`/`Route`."""
from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.contribution import Contribution
from backend.models.enums import ContributionStatus, ContributionTargetType


async def create(
    db: AsyncSession,
    *,
    target_type: ContributionTargetType,
    submitted_by_id: uuid.UUID,
    stop_id: uuid.UUID | None = None,
    route_id: uuid.UUID | None = None,
    status: ContributionStatus = ContributionStatus.PENDING,
) -> Contribution:
    contribution = Contribution(
        target_type=target_type,
        stop_id=stop_id,
        route_id=route_id,
        submitted_by_id=submitted_by_id,
        status=status,
    )
    db.add(contribution)
    await db.flush()
    await db.refresh(contribution)
    return contribution


async def get_original_submitter_id(
    db: AsyncSession,
    *,
    target_type: ContributionTargetType,
    target_id: uuid.UUID,
) -> uuid.UUID | None:
    """
    Who first submitted this stop/route -- the earliest `Contribution` row
    for it. Used by edit-permission checks (`can_edit` in the stop/route
    services) since neither `Stop` nor `Route` stores this itself.
    """
    target_column = (
        Contribution.stop_id if target_type is ContributionTargetType.STOP else Contribution.route_id
    )
    result = await db.execute(
        select(Contribution.submitted_by_id)
        .where(target_column == target_id, Contribution.target_type == target_type)
        .order_by(Contribution.created_at.asc())
        .limit(1)
    )
    return result.scalar_one_or_none()
