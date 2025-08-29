from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None

class TokenPayload(BaseModel):
    sub: str
    exp: int
    type: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str