import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()

REQUIRED_ENV_VARS = ("OPENAI_API_KEY", "BAIDU_MAPS_API_KEY")


def check_required_env_vars():
    missing = [v for v in REQUIRED_ENV_VARS if not os.environ.get(v)]
    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}. "
            f"Please set them in your .env file. See .env.example for reference."
        )


check_required_env_vars()

from fastapi import FastAPI
from fastapi.responses import FileResponse
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from app.agents import build_agent
from app.api.v1 import router as api_v1_router
from app.db import DB_PATH


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncSqliteSaver.from_conn_string(DB_PATH) as checkpointer:
        app.state.checkpointer = checkpointer
        app.state.agent_app = build_agent(checkpointer)
        yield


app = FastAPI(lifespan=lifespan)

# Include API routes
app.include_router(api_v1_router)


@app.get("/")
async def root():
    return FileResponse("static/index.html")