from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=6)


class LoginRequest(BaseModel):
    username: str = Field(...)
    password: str = Field(...)


class AuthResponse(BaseModel):
    token: str
    user: "UserInfo"


class UserInfo(BaseModel):
    id: int
    username: str
    nickname: str
    avatar_url: str | None = None


class UserProfile(BaseModel):
    """User profile with full details including timestamps."""
    id: int
    username: str
    nickname: str
    avatar_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UpdateProfileRequest(BaseModel):
    nickname: str = Field(..., min_length=1, max_length=20)