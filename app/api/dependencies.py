from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import AuthService
from app.services.container_service import ContainerService
from app.schemas.user import UserResponse
from app.core.exceptions import CredentialsException

security = HTTPBearer()


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)


def get_container_service(db: Session = Depends(get_db)) -> ContainerService:
    return ContainerService(db)


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        auth_service: AuthService = Depends(get_auth_service)
) -> UserResponse:

    token = credentials.credentials

    try:
        user = auth_service.get_current_user(token)
        return UserResponse.from_orm(user)
    except Exception as e:
        raise CredentialsException(str(e))
