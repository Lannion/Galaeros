# backend/app/models/route.py
"""
Route Domain Model (PostGIS LineString).

A single named commuting route (one jeepney line, one bus route, etc.).
The ordered sequence of stops that actually defines the route lives in
RouteStop, not here — `path` is a rendering/distance convenience derived
from that sequence, not the source of truth (see route_stop.py and
ARCHITECTURE.md > Routing Engine, where each stop is a node and each
route a set of edges).
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from geoalchemy2 import Geometry
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin
from .enums import RouteStatus, VehicleType

if TYPE_CHECKING:
    from .route_stop import RouteStop


# Add Index to your imports
from sqlalchemy import Numeric, String, Index 
# ... keep other imports

class Route(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    """A single commuting route, e.g. 'SM Bacoor - PITX via Aguinaldo Hwy'."""

    __tablename__ = "routes"

    name: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    vehicle_type: Mapped[VehicleType] = mapped_column(
        SQLEnum(
            VehicleType,
            name="vehicle_type",
            native_enum=True,
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
        index=True,
    )
    status: Mapped[RouteStatus] = mapped_column(
        SQLEnum(
            RouteStatus,
            name="route_status",
            native_enum=True,
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        default=RouteStatus.PENDING,
        server_default=RouteStatus.PENDING.value,
        nullable=False,
        index=True,
    )

    base_fare: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True)

    # --- Path geometry ---
    path: Mapped[str | None] = mapped_column(
        Geometry(geometry_type="LINESTRING", srid=4326, spatial_index=False),
        nullable=True,
    )

    # Move __table_args__ here (after 'path' is declared)
    __table_args__ = (
        Index("idx_routes_path", "path", postgresql_using="gist"),
    )

    # --- Relationships ---
    stop_links: Mapped[list["RouteStop"]] = relationship(
        "RouteStop",
        back_populates="route",
        cascade="all, delete-orphan",
        order_by="RouteStop.sequence",
    )

    def __repr__(self) -> str:
        return f"<Route id={self.id} name={self.name!r} status={self.status}>"