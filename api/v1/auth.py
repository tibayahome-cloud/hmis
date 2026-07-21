from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from schemas.auth import AccessToken, LoginRequest, RefreshRequest, TokenPair
from services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenPair)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    staff = await auth_service.authenticate_staff(db, payload.email, payload.password)
    return await auth_service.issue_token_pair(staff)


@router.post("/refresh", response_model=AccessToken)
async def refresh(payload: RefreshRequest, db: AsyncSession = Depends(get_db)):
    return await auth_service.refresh_access_token(db, payload.refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout():
    # Access/refresh tokens are stateless JWTs in this design — logout is enforced
    # client-side (discard tokens). If server-side revocation is needed later,
    # swap in a Redis-backed denylist keyed on the token's jti here.
    return None
