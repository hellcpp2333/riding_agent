from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.utils import decode_token
import app.db_mysql as db_mysql
from app.models import User
from app.redis_client import get_session

security = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> User:
    if credentials is None:
        raise HTTPException(status_code=401, detail="未登录")

    token = credentials.credentials

    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="登录已过期")

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="登录已过期")
    user_id = int(user_id)

    session_user_id = await get_session(token)
    if session_user_id is None or session_user_id != user_id:
        raise HTTPException(status_code=401, detail="登录已失效")

    assert db_mysql.async_session_factory is not None
    async with db_mysql.async_session_factory() as db:
        user = await db.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=401, detail="用户不存在")
        return user