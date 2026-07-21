from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPKMixin


class Role(UUIDPKMixin, TimestampMixin, Base):
    """
    One of: admin, receptionist, billing_clerk, triage_nurse, doctor, lab_tech,
    pharmacist, admission_officer, ward_nurse, consultant, records_officer.
    Seeded via alembic data migration, not user-creatable via API.
    """

    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    staff: Mapped[list["Staff"]] = relationship(back_populates="role")
