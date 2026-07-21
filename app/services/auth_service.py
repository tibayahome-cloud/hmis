from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import UnauthorizedError
from app.core.security import (
    InvalidTokenError,
    TokenType,
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)
from app.models.staff import Staff
from app.schemas.auth import AccessToken, TokenPair


async def authenticate_staff(db: AsyncSession, email: str, password: str) -> Staff:
    result = await db.execute(
        select(Staff).options(selectinload(Staff.role)).where(Staff.email == email)
    )
    staff = result.scalar_one_or_none()
    if staff is None or not staff.is_active or not verify_password(password, staff.hashed_password):
        raise UnauthorizedError("Incorrect email or password")
    return staff


async def issue_token_pair(staff: Staff) -> TokenPair:
    return TokenPair(
        access_token=create_access_token(staff.id),
        refresh_token=create_refresh_token(staff.id),
    )


async def refresh_access_token(db: AsyncSession, refresh_token: str) -> AccessToken:
    try:
        staff_id = decode_token(refresh_token, TokenType.REFRESH)
    except InvalidTokenError as exc:
        raise UnauthorizedError(str(exc)) from exc

    result = await db.execute(
        select(Staff).where(Staff.id == staff_id).where(Staff.is_active.is_(True))
    )
    staff = result.scalar_one_or_none()
    if staff is None:
        raise UnauthorizedError("Staff not found or inactive")

    return AccessToken(access_token=create_access_token(staff.id))
