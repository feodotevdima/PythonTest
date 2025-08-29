from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.user import UserLogin
from app.schemas.token import Token, RefreshTokenRequest
from app.api.dependencies import get_auth_service
from app.database import get_db
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login", response_model=Token)
def login(
    user_data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
):
    return auth_service.login(user_data)

@router.post("/refresh", response_model=Token)
def refresh_tokens(
    refresh_request: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    return auth_service.refresh_tokens(refresh_request.refresh_token)
