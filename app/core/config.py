import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/minipos.db")
SECRET_KEY = os.getenv("SECRET_KEY", "").strip()
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "480"))
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "*").split(",")
    if origin.strip()
]

_INVALID_SECRET_KEYS = {
    "change-this-secret-key",
    "change-this-development-secret",
    "replace-this-with-a-long-random-secret",
    "change-this-to-a-long-random-secret-before-running",
}

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is required. Create a .env file before running the API.")

if SECRET_KEY in _INVALID_SECRET_KEYS or len(SECRET_KEY) < 32:
    raise RuntimeError("SECRET_KEY must be changed to a private value with at least 32 characters.")
