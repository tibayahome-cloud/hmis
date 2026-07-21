from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPKMixin


class Hospital(UUIDPKMixin, TimestampMixin, Base):
    """A tenant. Every Staff (except super_admin) belongs to exactly one Hospital,
    and from Day 2 onward every clinical/financial record hangs off a hospital_id
    somewhere up its chain (directly, or via visit -> patient's registering hospital)."""

    __tablename__ = "hospitals"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, index=True)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    staff: Mapped[list["Staff"]] = relationship(back_populates="hospital")
