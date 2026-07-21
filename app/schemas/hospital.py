import uuid

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.auth import StaffRead


class HospitalCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    code: str = Field(min_length=2, max_length=30, description="Short unique tenant code, e.g. 'NRB-001'")
    address: str | None = None
    phone: str | None = None

    admin_full_name: str = Field(min_length=2, max_length=150)
    admin_email: EmailStr
    admin_password: str = Field(min_length=8)


class HospitalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    code: str
    address: str | None
    phone: str | None
    is_active: bool


class HospitalWithAdminRead(BaseModel):
    hospital: HospitalRead
    admin: StaffRead
