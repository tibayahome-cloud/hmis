import uuid

import pytest

from app.core.security import (
    InvalidTokenError,
    TokenType,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)


def test_password_hash_roundtrip():
    hashed = hash_password("s3cret-password")
    assert verify_password("s3cret-password", hashed)
    assert not verify_password("wrong-password", hashed)


def test_access_token_roundtrip():
    staff_id = uuid.uuid4()
    token = create_access_token(staff_id)
    assert decode_token(token, TokenType.ACCESS) == staff_id


def test_refresh_token_rejected_as_access_token():
    staff_id = uuid.uuid4()
    token = create_refresh_token(staff_id)
    with pytest.raises(InvalidTokenError):
        decode_token(token, TokenType.ACCESS)


def test_garbage_token_rejected():
    with pytest.raises(InvalidTokenError):
        decode_token("not-a-real-token", TokenType.ACCESS)
