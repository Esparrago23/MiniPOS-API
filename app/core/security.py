import base64
import hashlib
import hmac
import json
import os
import time

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY

_HASH_ITERATIONS = 120_000


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        _HASH_ITERATIONS,
    )
    return "$".join(
        [
            str(_HASH_ITERATIONS),
            _to_base64_url(salt),
            _to_base64_url(password_hash),
        ],
    )


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        iterations_text, salt_text, hash_text = stored_hash.split("$")
        iterations = int(iterations_text)
        salt = _from_base64_url(salt_text)
        expected_hash = _from_base64_url(hash_text)
    except ValueError:
        return False

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations,
    )
    return hmac.compare_digest(password_hash, expected_hash)


def create_access_token(user_id: int) -> str:
    expires_at = int(time.time()) + ACCESS_TOKEN_EXPIRE_MINUTES * 60
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"sub": str(user_id), "exp": expires_at}

    header_text = _json_to_base64_url(header)
    payload_text = _json_to_base64_url(payload)
    signature = hmac.new(
        SECRET_KEY.encode("utf-8"),
        f"{header_text}.{payload_text}".encode("utf-8"),
        hashlib.sha256,
    ).digest()

    return f"{header_text}.{payload_text}.{_to_base64_url(signature)}"


def decode_access_token(token: str) -> int | None:
    try:
        header_text, payload_text, signature_text = token.split(".")
        expected_signature = hmac.new(
            SECRET_KEY.encode("utf-8"),
            f"{header_text}.{payload_text}".encode("utf-8"),
            hashlib.sha256,
        ).digest()

        if not hmac.compare_digest(
            _to_base64_url(expected_signature),
            signature_text,
        ):
            return None

        payload = json.loads(_from_base64_url(payload_text))
        expires_at = int(payload["exp"])
        if expires_at < int(time.time()):
            return None

        return int(payload["sub"])
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        return None


def _json_to_base64_url(value: dict[str, object]) -> str:
    raw = json.dumps(value, separators=(",", ":")).encode("utf-8")
    return _to_base64_url(raw)


def _to_base64_url(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("utf-8").rstrip("=")


def _from_base64_url(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)
