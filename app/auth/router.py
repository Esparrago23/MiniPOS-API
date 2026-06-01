from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import UserModel
from app.auth.repository import AuthRepository
from app.auth.schemas import (
    AuthResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from app.auth.service import AuthService
from app.core.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(AuthRepository(db))


@router.post("/register", response_model=AuthResponse, status_code=201)
def register(
    request: UserRegisterRequest,
    service: AuthService = Depends(get_auth_service),
) -> AuthResponse:
    token, user = service.register(request)
    return AuthResponse(token=token, user=user)


@router.post("/login", response_model=AuthResponse)
def login(
    request: UserLoginRequest,
    service: AuthService = Depends(get_auth_service),
) -> AuthResponse:
    token, user = service.login(request)
    return AuthResponse(token=token, user=user)


@router.get("/me", response_model=UserResponse)
def me(current_user: UserModel = Depends(get_current_user)) -> UserModel:
    return current_user
