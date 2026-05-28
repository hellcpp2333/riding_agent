from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.auth.dependencies import get_current_user
from app.auth.schemas import UpdateProfileRequest, UserInfo, UserProfile
import app.db_mysql as db_mysql
from app.models import User
from app.services.oss_service import upload_avatar

router = APIRouter(prefix="/api/user", tags=["user"])


@router.get("/profile", response_model=UserProfile)
async def get_profile(user: User = Depends(get_current_user)) -> UserProfile:
    assert db_mysql.async_session_factory is not None
    async with db_mysql.async_session_factory() as db:
        u = await db.get(User, user.id)
        return UserProfile(
            id=u.id,
            username=u.username,
            nickname=u.nickname,
            avatar_url=u.avatar_url,
            created_at=u.created_at,
            updated_at=u.updated_at,
        )


@router.put("/profile", response_model=UserInfo)
async def update_profile(
    req: UpdateProfileRequest, user: User = Depends(get_current_user)
) -> UserInfo:
    assert db_mysql.async_session_factory is not None
    async with db_mysql.async_session_factory() as db:
        u = await db.get(User, user.id)
        u.nickname = req.nickname
        await db.commit()
        await db.refresh(u)
        return UserInfo(
            id=u.id,
            username=u.username,
            nickname=u.nickname,
            avatar_url=u.avatar_url,
        )


@router.post("/avatar", response_model=dict)
async def upload_profile_avatar(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
) -> dict:
    if file.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(status_code=400, detail="仅支持 jpg/png 格式")

    file_data = await file.read()
    if len(file_data) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="文件大小不能超过 5MB")

    try:
        avatar_url = upload_avatar(file_data, file.filename or "avatar.jpg", user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    assert db_mysql.async_session_factory is not None
    async with db_mysql.async_session_factory() as db:
        u = await db.get(User, user.id)
        u.avatar_url = avatar_url
        await db.commit()

    return {"avatar_url": avatar_url}