from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import ConflictError, NotFoundError
from app.core.security import hash_password
from app.models.role import Role
from app.models.staff import Staff
from app.schemas.auth import StaffCreate


async def create_staff(db: AsyncSession, payload: StaffCreate) -> Staff:
    existing = await db.execute(select(Staff).where(Staff.email == payload.email))
    if existing.scalar_one_or_none() is not None:
        raise ConflictError(f"A staff member with email '{payload.email}' already exists")

    role = await db.get(Role, payload.role_id)
    if role is None:
        raise NotFoundError(f"Role '{payload.role_id}' not found")

    staff = Staff(
        full_name=payload.full_name,
        email=payload.email,
        phone=payload.phone,
        hashed_password=hash_password(payload.password),
        role_id=role.id,
    )
    db.add(staff)
    await db.commit()
    await db.refresh(staff, attribute_names=["role"])
    return staff


async def get_staff(db: AsyncSession, staff_id) -> Staff:
    result = await db.execute(
        select(Staff).options(selectinload(Staff.role)).where(Staff.id == staff_id)
    )
    staff = result.scalar_one_or_none()
    if staff is None:
        raise NotFoundError("Staff not found")
    return staff


async def list_staff(db: AsyncSession, limit: int = 50, cursor: str | None = None) -> list[Staff]:
    query = select(Staff).options(selectinload(Staff.role)).order_by(Staff.created_at.desc())
    if cursor:
        query = query.where(Staff.id < cursor)
    query = query.limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


async def list_roles(db: AsyncSession) -> list[Role]:
    result = await db.execute(select(Role).order_by(Role.name))
    return list(result.scalars().all())
