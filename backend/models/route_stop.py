# backend/app/models/route_stop.py
"""
RouteStop Association Model (Ordered junction between Route and Stop).

A route is an ORDERED sequence of stops — a plain many-to-many table isn't
enough, since "Stop A then Stop B" is a different route than "Stop B then
Stop A". This association object carries that ordering (`sequence`) plus
per-segment detail (fare and distance to the next stop on the route),
matching ARCHITECTURE.md > Routing Engine's model of stops as nodes and
routes as edges between them.
"""
from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Numeric, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from .route import Route
    from .stop import Stop


class RouteStop(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """
    One stop's ordered position within a route.

    Not soft-deletable on its own — a route's stop ordering changes by
    inserting/removing these junction rows directly (cascaded automatically
    if the parent Route or Stop is hard-deleted). The Route and Stop
    themselves remain independently soft-deletable.
    """

    __tablename__ = "route_stops"
    __table_args__ = (
        UniqueConstraint("route_id", "sequence", name="uq_route_stop_sequence"),
    )

    route_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("routes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    stop_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("stops.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # --- Ordering ---
    # Position of this stop within the route, starting at 0. Unique per
    # route (see __table_args__) so a sequence can never have gaps/dupes.
    sequence: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    # --- Per-segment detail: this stop -> the next stop in the sequence ---
    fare_to_next_stop: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True)
    distance_meters_to_next_stop: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # --- Relationships ---
    route: Mapped["Route"] = relationship(back_populates="stop_links")
    stop: Mapped["Stop"] = relationship(back_populates="route_links")

    def __repr__(self) -> str:
        return f"<RouteStop route_id={self.route_id} stop_id={self.stop_id} sequence={self.sequence}>"