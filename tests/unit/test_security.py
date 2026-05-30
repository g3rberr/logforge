from core.security import create_token, decode_token, hash_password, verify_password


def test_password_hashing() -> None:
    password = "test-password-123"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed) is True


def test_password_hashing_wrong() -> None:
    hashed = hash_password("correct")
    assert verify_password("wrong", hashed) is False


def test_jwt_token_roundtrip() -> None:
    user_id = "test-user-id-123"
    token = create_token(user_id)
    assert token is not None

    decoded = decode_token(token)
    assert decoded == user_id


def test_jwt_invalid_token() -> None:
    assert decode_token("invalid-token") is None
