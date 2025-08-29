from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password
from app.core.jwt import create_access_token, create_refresh_token, verify_token
from app.schemas.user import UserLogin
from app.core.exceptions import CredentialsException


class AuthService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def authenticate_user(self, username: str, password: str):
        user = self.user_repository.get_by_username(username)
        if not user or not verify_password(password, user.password_hash):
            return None
        return user

    def login(self, user_data: UserLogin):
        user = self.authenticate_user(user_data.username, user_data.password)
        if not user:
            raise CredentialsException("Incorrect username or password")

        access_token = create_access_token({"sub": user.username})
        refresh_token = create_refresh_token({"sub": user.username})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    def refresh_tokens(self, refresh_token: str):
        payload = verify_token(refresh_token)
        if payload.get("type") != "refresh":
            raise CredentialsException("Invalid token type - expected refresh token")

        username = payload.get("sub")
        user = self.user_repository.get_by_username(username)
        if not user:
            raise CredentialsException("User not found")

        access_token = create_access_token({"sub": user.username})
        new_refresh_token = create_refresh_token({"sub": user.username})

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }

    def get_current_user(self, token: str):
        payload = verify_token(token)

        if payload.get("type") != "access":
            raise CredentialsException("Invalid token type - expected access token")

        username = payload.get("sub")
        if username is None:
            raise CredentialsException("Invalid token payload - missing subject")

        user = self.user_repository.get_by_username(username)
        if user is None:
            raise CredentialsException("User not found")

        return user