from datetime import timedelta
from typing import Optional

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.domain.exceptions import UnauthorizedError
from app.domain.schemas import Token, UserCreate, UserRead
from app.infrastructure.auth.jwt import create_access_token
from app.infrastructure.config import get_settings
from app.infrastructure.db.repositories import UserRepository


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)
        self.settings = get_settings()

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def _hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def register_user(self, payload: UserCreate) -> UserRead:
        existing = self.users.get_by_email(payload.email)
        if existing:
            raise UnauthorizedError("El usuario ya existe")
        hashed = self._hash_password(payload.password)
        user = self.users.create(email=payload.email, hashed_password=hashed)
        return UserRead.model_validate(user)

    def authenticate_user(self, email: str, password: str) -> Optional[UserRead]:
        user = self.users.get_by_email(email)
        if not user:
            return None
        if not self._verify_password(password, user.hashed_password):
            return None
        return UserRead.model_validate(user)

    def login(self, email: str, password: str) -> Token:
        user = self.authenticate_user(email, password)
        if not user:
            raise UnauthorizedError("Credenciales inválidas")

        access_token_expires = timedelta(
            minutes=self.settings.access_token_expire_minutes
        )
        access_token = create_access_token(
            subject=user.email,
            expires_delta=access_token_expires,
        )
        return Token(access_token=access_token)

