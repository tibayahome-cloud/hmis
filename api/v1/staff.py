import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.rbac import get_current_staff, require_roles
from db.session import get_db
from schemas.auth import RoleRead, StaffCreate, StaffRead
from services import staff_service

router = APIRouter(prefix="/staff", tags=["staff"])


@router.post("", response_model=StaffRead, status_code=201)
async def create_staff(
    payload: StaffCreate,
    db: AsyncSession = Depends(get_db),
    acting_admin=Depends(require_roles("admin")),
):
    return await staff_service.create_staff(db, payload, acting_admin)


@router.get("/me", response_model=StaffRead)
async def get_me(current=Depends(get_current_staff)):
    return current


@router.get("", response_model=list[StaffRead])
async def list_staff(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(50, le=200),
    cursor: uuid.UUID | None = None,
    acting_staff=Depends(require_roles("admin", "super_admin")),
):
    return await staff_service.list_staff(
        db, acting_staff, limit=limit, cursor=str(cursor) if cursor else None
    )


@router.get("/{staff_id}", response_model=StaffRead)
async def get_staff(
    staff_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    acting_staff=Depends(require_roles("admin", "super_admin")),
):
    return await staff_service.get_staff(db, staff_id, acting_staff)


@router.get("/roles/list", response_model=list[RoleRead])
async def get_roles(db: AsyncSession = Depends(get_db), current=Depends(get_current_staff)):
    return await staff_service.list_roles(db)
