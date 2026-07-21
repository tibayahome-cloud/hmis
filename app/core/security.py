import uuid
from datetime import datetime, timedelta, timezone
from enum import Enum

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def _create_token(subject: uuid.UUID, token_type: TokenType, expires_delta: timedelta) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(subject),
        "type": token_type.value,
        "iat": now,
        "exp": now + expires_delta,
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_access_token(staff_id: uuid.UUID) -> str:
    return _create_token(
        staff_id, TokenType.ACCESS, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )


def create_refresh_token(staff_id: uuid.UUID) -> str:
    return _create_token(
        staff_id, TokenType.REFRESH, timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )


class InvalidTokenError(Exception):
    pass


def decode_token(token: str, expected_type: TokenType) -> uuid.UUID:
    """Decode a JWT and return the staff_id, raising InvalidTokenError on any problem."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except JWTError as exc:
        raise InvalidTokenError("Could not validate token") from exc

    if payload.get("type") != expected_type.value:
        raise InvalidTokenError(f"Expected a {expected_type.value} token")

    subject = payload.get("sub")
    if subject is None:
        raise InvalidTokenError("Token missing subject")

    try:
        return uuid.UUID(subject)
    except ValueError as exc:
        raise InvalidTokenError("Token subject is not a valid UUID") from exc
