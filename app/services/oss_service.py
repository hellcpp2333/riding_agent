import os
import time
import uuid

import oss2

OSS_ACCESS_KEY_ID = os.environ.get("OSS_ACCESS_KEY_ID", "")
OSS_ACCESS_KEY_SECRET = os.environ.get("OSS_ACCESS_KEY_SECRET", "")
OSS_BUCKET_NAME = os.environ.get("OSS_BUCKET_NAME", "")
OSS_ENDPOINT = os.environ.get("OSS_ENDPOINT", "oss-cn-shenzhen.aliyuncs.com")

MAX_AVATAR_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def upload_avatar(file_data: bytes, filename: str, user_id: int) -> str:
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("仅支持 jpg/png 格式")

    if len(file_data) > MAX_AVATAR_SIZE:
        raise ValueError("文件大小不能超过 5MB")

    auth = oss2.Auth(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET_NAME)

    object_key = (
        f"avatars/{user_id}/{int(time.time())}_{uuid.uuid4().hex[:8]}{ext}"
    )
    bucket.put_object(object_key, file_data)

    return f"https://{OSS_BUCKET_NAME}.{OSS_ENDPOINT}/{object_key}"