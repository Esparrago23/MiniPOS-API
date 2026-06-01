from sqlalchemy.orm import Session

from app.auth.models import UserModel


class AuthRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_email(self, email: str) -> UserModel | None:
        return self._db.query(UserModel).filter(UserModel.email == email).first()

    def get_by_id(self, user_id: int) -> UserModel | None:
        return self._db.query(UserModel).filter(UserModel.id == user_id).first()

    def create_user(
        self,
        *,
        name: str,
        email: str,
        password_hash: str,
    ) -> UserModel:
        user = UserModel(
            name=name,
            email=email,
            password_hash=password_hash,
        )
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user
