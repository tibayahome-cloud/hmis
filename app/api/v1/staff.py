import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.rbac import get_current_staff, require_roles
from app.db.session import get_db
from app.schemas.auth import RoleRead, StaffCreate, StaffRead
from app.services import staff_service

router = APIRouter(prefix="/staff", tags=["staff"])


@router.post("", response_model=StaffRead, status_code=201, dependencies=[Depends(require_roles("admin"))])
async def create_staff(payload: StaffCreate, db: AsyncSession = Depends(get_db)):
    return await staff_service.create_staff(db, payload)


@router.get("/me", response_model=StaffRead)
async def get_me(current=Depends(get_current_staff)):
    return current


@router.get("", response_model=list[StaffRead], dependencies=[Depends(require_roles("admin"))])
async def list_staff(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(50, le=200),
    cursor: uuid.UUID | None = None,
):
    return await staff_service.list_staff(db, limit=limit, cursor=str(cursor) if cursor else None)


@router.get("/{staff_id}", response_model=StaffRead, dependencies=[Depends(require_roles("admin"))])
async def get_staff(staff_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await staff_service.get_staff(db, staff_id)


@router.get("/roles/list", response_model=list[RoleRead])
async def get_roles(db: AsyncSession = Depends(get_db), current=Depends(get_current_staff)):
    return await staff_service.list_roles(db)
