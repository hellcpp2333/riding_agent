import json
import os

import redis.asyncio as redis

REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "") or None

redis_client: redis.Redis | None = None

SESSION_TTL = 86400  # 24 hours
STATUS_TTL = 300  # 5 minutes


def init_redis() -> redis.Redis:
    global redis_client
    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        decode_responses=True,
    )
    return redis_client


async def close_redis() -> None:
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None


def _ensure_client() -> redis.Redis:
    assert redis_client is not None, "Redis client not initialized"
    return redis_client


async def create_session(token: str, user_id: int) -> None:
    key = f"auth:session:{token}"
    data = json.dumps({"user_id": user_id})
    await _ensure_client().setex(key, SESSION_TTL, data)


async def get_session(token: str) -> int | None:
    key = f"auth:session:{token}"
    data = await _ensure_client().get(key)
    if data:
        info = json.loads(data)
        return info.get("user_id")
    return None


async def delete_session(token: str) -> None:
    key = f"auth:session:{token}"
    await _ensure_client().delete(key)


async def set_user_status(user_id: int, online: bool) -> None:
    key = f"auth:user:{user_id}:status"
    data = json.dumps({"online": online})
    await _ensure_client().setex(key, STATUS_TTL, data)


async def get_user_status(user_id: int) -> dict | None:
    key = f"auth:user:{user_id}:status"
    data = await _ensure_client().get(key)
    if data:
        return json.loads(data)
    return None
