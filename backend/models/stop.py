# backend/app/models/stop.py
"""
Stop Domain Model (PostGIS Point).

A single physical location where commuters board or alight a vehicle:
a standard stop, terminal, interchange, port, or airport. Location is
stored as a PostGIS POINT so proximity search ("nearest stops to me")
and map rendering can use PostGIS's geographic query support directly,
per ARCHITECTURE.md > Database Design.
"""

from typing import TYPE_CHECKING

from geoalchemy2 import Geometry
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, SoftDeleteMixin, TimestampMixin, UUIDPrimaryKeyMixin
from .enums import StopType

if TYPE_CHECKING:
    from .route_stop import RouteStop


class Stop(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin):
    """A physical transit stop, terminal, interchange, port, or airport."""

    __tablename__ = "stops"

    name: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    stop_type: Mapped[StopType] = mapped_column(
        SQLEnum(
            StopType,
            name="stop_type",
            native_enum=True,
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        default=StopType.STANDARD,
        server_default=StopType.STANDARD.value,
        nullable=False,
        index=True,
    )

    # --- Location (PostGIS) ---
    # SRID 4326 = WGS 84, the coordinate system GPS devices report in.
    # Needs a GiST index (created via Alembic migration) for proximity
    # queries to stay fast at nationwide scale.
    location: Mapped[str] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=False),
        nullable=False,
    )

    __table_args__ = (
        Index("idx_stops_location", "location", postgresql_using="gist"),
    )

    # --- Administrative context (see ARCHITECTURE.md > Database Overview) ---
    city: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    barangay: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)

    # --- Relationships ---
    route_links: Mapped[list["RouteStop"]] = relationship(
        back_populates="stop",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Stop id={self.id} name={self.name!r} type={self.stop_type}>"