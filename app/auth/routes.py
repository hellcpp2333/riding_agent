from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select

from app.auth.dependencies import get_current_user
from app.auth.schemas import (
    AuthResponse,
    LoginRequest,
    RegisterRequest,
    UserInfo,
)
from app.auth.utils import create_access_token, hash_password, verify_password
import app.db_mysql as db_mysql
from app.models import User
from app.redis_client import create_session, delete_session, set_user_status

router = APIRouter(prefix="/api/auth", tags=["auth"])

_bearer = HTTPBearer(auto_error=False)


async def _extract_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> str:
    if credentials:
        return credentials.credentials
    return ""


@router.post("/register", status_code=201)
async def register(req: RegisterRequest) -> AuthResponse:
    assert db_mysql.async_session_factory is not None
    async with db_mysql.async_session_factory() as db:
        existing = (
            await db.execute(
                select(User).where(User.username == req.username)
            )
        ).scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=409, detail="用户名已被注册")

        user = User(
            username=req.username,
            password_hash=hash_password(req.password),
            nickname=req.username,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

        token = create_access_token(user.id, user.username)
        await create_session(token, user.id)
        await set_user_status(user.id, online=True)

        return AuthResponse(
            token=token,
            user=UserInfo(
                id=user.id,
                username=user.username,
                nickname=user.nickname,
                avatar_url=user.avatar_url,
            ),
        )


@router.post("/login")
async def login(req: LoginRequest) -> AuthResponse:
    assert db_mysql.async_session_factory is not None
    async with db_mysql.async_session_factory() as db:
        result = await db.execute(
            select(User).where(User.username == req.username)
        )
        user = result.scalar_one_or_none()

        if user is None or not verify_password(req.password, user.password_hash):
            raise HTTPException(status_code=401, detail="用户名或密码错误")

        token = create_access_token(user.id, user.username)
        await create_session(token, user.id)
        await set_user_status(user.id, online=True)

        return AuthResponse(
            token=token,
            user=UserInfo(
                id=user.id,
                username=user.username,
                nickname=user.nickname,
                avatar_url=user.avatar_url,
            ),
        )


@router.post("/logout")
async def logout(
    user: User = Depends(get_current_user),
    token: str = Depends(_extract_token),
) -> dict:
    await delete_session(token)
    await set_user_status(user.id, online=False)
    return {"message": "已退出登录"}


@router.get("/me", response_model=UserInfo)
async def me(user: User = Depends(get_current_user)) -> UserInfo:
    return UserInfo(
        id=user.id,
        username=user.username,
        nickname=user.nickname,
        avatar_url=user.avatar_url,
    )