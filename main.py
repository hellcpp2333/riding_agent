import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()

REQUIRED_ENV_VARS = ("OPENAI_API_KEY", "LLM_MODEL", "BAIDU_MAPS_API_KEY", "BAIDU_MAPS_JS_AK")


def check_required_env_vars():
    missing = [v for v in REQUIRED_ENV_VARS if not os.environ.get(v)]
    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}. "
            f"Please set them in your .env file. See .env.example for reference."
        )


check_required_env_vars()

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from app.agents import build_agent
from app.api.v1 import router as api_v1_router
from app.auth.routes import router as auth_router
from app.api.v1.user_routes import router as user_router
from app.db import DB_PATH
from app.db_mysql import dispose_mysql, init_db, init_mysql_engine
from app.redis_client import close_redis, init_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize MySQL
    init_mysql_engine()
    await init_db()

    # Initialize Redis
    init_redis()

    async with AsyncSqliteSaver.from_conn_string(DB_PATH) as checkpointer:
        app.state.checkpointer = checkpointer
        app.state.agent_app = build_agent(checkpointer)
        yield

    # Cleanup
    await dispose_mysql()
    await close_redis()


app = FastAPI(lifespan=lifespan)

# Include API routes
app.include_router(api_v1_router)
app.include_router(auth_router)
app.include_router(user_router)


@app.get("/")
async def root():
    html_path = "static/index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    html = html.replace("__BAIDU_MAPS_JS_AK__", os.environ["BAIDU_MAPS_JS_AK"])
    return HTMLResponse(content=html)
