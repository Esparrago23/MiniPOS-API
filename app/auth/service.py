from fastapi import HTTPException, status

from app.auth.models import UserModel
from app.auth.repository import AuthRepository
from app.auth.schemas import UserLoginRequest, UserRegisterRequest
from app.core.security import create_access_token, hash_password, verify_password


class AuthService:
    def __init__(self, repository: AuthRepository) -> None:
        self._repository = repository

    def register(self, request: UserRegisterRequest) -> tuple[str, UserModel]:
        existing_user = self._repository.get_by_email(request.email)
        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered.",
            )

        user = self._repository.create_user(
            name=request.name,
            email=request.email,
            password_hash=hash_password(request.password),
        )
        return create_access_token(user.id), user

    def login(self, request: UserLoginRequest) -> tuple[str, UserModel]:
        user = self._repository.get_by_email(request.email)
        if user is None or not verify_password(request.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        return create_access_token(user.id), user
