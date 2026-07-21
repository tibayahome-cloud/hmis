from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import ConflictError, NotFoundError
from app.core.security import hash_password
from app.models.hospital import Hospital
from app.models.role import Role
from app.models.staff import Staff
from app.schemas.hospital import HospitalCreate


async def create_hospital_with_admin(db: AsyncSession, payload: HospitalCreate) -> tuple[Hospital, Staff]:
    existing_code = await db.execute(select(Hospital).where(Hospital.code == payload.code))
    if existing_code.scalar_one_or_none() is not None:
        raise ConflictError(f"A hospital with code '{payload.code}' already exists")

    existing_email = await db.execute(select(Staff).where(Staff.email == payload.admin_email))
    if existing_email.scalar_one_or_none() is not None:
        raise ConflictError(f"A staff member with email '{payload.admin_email}' already exists")

    admin_role = (await db.execute(select(Role).where(Role.name == "admin"))).scalar_one_or_none()
    if admin_role is None:
        raise NotFoundError("'admin' role is not seeded — run migrations")

    hospital = Hospital(
        name=payload.name,
        code=payload.code,
        address=payload.address,
        phone=payload.phone,
    )
    db.add(hospital)
    await db.flush()  # get hospital.id without committing yet

    admin = Staff(
        full_name=payload.admin_full_name,
        email=payload.admin_email,
        hashed_password=hash_password(payload.admin_password),
        role_id=admin_role.id,
        hospital_id=hospital.id,
    )
    db.add(admin)

    await db.commit()
    await db.refresh(hospital)
    await db.refresh(admin, attribute_names=["role"])
    return hospital, admin


async def list_hospitals(db: AsyncSession, limit: int = 50) -> list[Hospital]:
    result = await db.execute(select(Hospital).order_by(Hospital.created_at.desc()).limit(limit))
    return list(result.scalars().all())


async def get_hospital(db: AsyncSession, hospital_id) -> Hospital:
    hospital = await db.get(Hospital, hospital_id)
    if hospital is None:
        raise NotFoundError("Hospital not found")
    return hospital
