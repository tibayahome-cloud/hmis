from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.security import InvalidTokenError, TokenType, decode_token
from app.db.session import get_db
from app.models.staff import Staff

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")


async def get_current_staff(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> Staff:
    """Resolve the JWT access token to an active Staff row, loading their role."""
    try:
        staff_id = decode_token(token, TokenType.ACCESS)
    except InvalidTokenError as exc:
        raise UnauthorizedError(str(exc)) from exc

    result = await db.execute(
        select(Staff).where(Staff.id == staff_id).where(Staff.is_active.is_(True))
    )
    staff = result.scalar_one_or_none()
    if staff is None:
        raise UnauthorizedError("Staff not found or inactive")
    # Ensure role is loaded for downstream role checks / response serialization
    await db.refresh(staff, attribute_names=["role"])
    return staff


def require_roles(*allowed_role_names: str):
    """
    Dependency factory used on every module's routers, e.g.:
        Depends(require_roles("billing_clerk", "admin"))
    "admin" is implicitly allowed everywhere it's meaningfully applicable is NOT
    assumed here — pass it explicitly per route if admins should bypass.
    """

    async def _check(staff: Staff = Depends(get_current_staff)) -> Staff:
        if staff.role.name not in allowed_role_names:
            raise ForbiddenError(
                f"Role '{staff.role.name}' is not permitted; requires one of {allowed_role_names}"
            )
        return staff

    return _check
