import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.rbac import require_roles
from db.session import get_db
from schemas.hospital import HospitalCreate, HospitalRead, HospitalWithAdminRead
from services import hospital_service

router = APIRouter(
    prefix="/hospitals", tags=["hospitals"], dependencies=[Depends(require_roles("super_admin"))]
)


@router.post("", response_model=HospitalWithAdminRead, status_code=201)
async def create_hospital(payload: HospitalCreate, db: AsyncSession = Depends(get_db)):
    hospital, admin = await hospital_service.create_hospital_with_admin(db, payload)
    return HospitalWithAdminRead(hospital=HospitalRead.model_validate(hospital), admin=admin)


@router.get("", response_model=list[HospitalRead])
async def list_hospitals(db: AsyncSession = Depends(get_db)):
    return await hospital_service.list_hospitals(db)


@router.get("/{hospital_id}", response_model=HospitalRead)
async def get_hospital(hospital_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await hospital_service.get_hospital(db, hospital_id)
