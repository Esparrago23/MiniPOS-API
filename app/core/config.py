import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./minipos.db")
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "480"))
