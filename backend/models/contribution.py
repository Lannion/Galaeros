"""
Contribution Domain Model.

Neither `Stop` nor `Route` tracks who created it or whether it's been
verified -- that's deliberate here: attribution and verification are their
own concern, separate from the transit data itself, per ARCHITECTURE.md's
Database Overview ("Everything revolves around Contributions, because
Galaeros is a community-driven platform") and the Community Verification
pipeline (duplicate check -> GPS validation -> community voting -> trusted
contributor review -> published).

A `Contribution` references exactly one of `stop_id` / `route_id` (enforced
by a CHECK constraint, not application code alone) and records who
submitted it, its current status, and who reviewed it. "Who created this
stop" is answered by querying for the `Contribution` with
`target_type=STOP, target_id=stop.id` and the earliest `created_at` --
there's no need to duplicate that onto `Stop` itself.

This intentionally does not yet model edit history (a second Contribution
row per subsequent edit) or community voting (individual votes toward
`status`) -- both are natural extensions once this shape is validated
against real usage, per the "never overengineer" principle in skills.md.
"""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from .enums import ContributionStatus, ContributionTargetType


class Contribution(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """One community submission: a new Stop, a new Route, or an edit to either."""

    __tablename__ = "contributions"
    __table_args__ = (
        CheckConstraint(
            "(stop_id IS NOT NULL AND route_id IS NULL) OR "
            "(stop_id IS NULL AND route_id IS NOT NULL)",
            name="ck_contributions_exactly_one_target",
        ),
    )

    target_type: Mapped[ContributionTargetType] = mapped_column(
        SQLEnum(
            ContributionTargetType,
            name="contribution_target_type",
            native_enum=True,
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
        index=True,
    )

    stop_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("stops.id", ondelete="CASCADE"), nullable=True, index=True
    )
    route_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("routes.id", ondelete="CASCADE"), nullable=True, index=True
    )

    status: Mapped[ContributionStatus] = mapped_column(
        SQLEnum(
            ContributionStatus,
            name="contribution_status",
            native_enum=True,
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        default=ContributionStatus.PENDING,
        server_default=ContributionStatus.PENDING.value,
        nullable=False,
        index=True,
    )

    submitted_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    reviewed_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    notes: Mapped[str | None] = mapped_column(String(500), nullable=True)

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        target = self.stop_id or self.route_id
        return f"<Contribution {self.target_type.value}={target} status={self.status.value}>"
