import json
from typing import AsyncGenerator

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from sse_starlette.sse import EventSourceResponse

import uuid

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from sse_starlette.sse import EventSourceResponse

from app.api.v1.schemas import ChatRequest, RoutePlanRequest
from app.db import list_sessions

router = APIRouter()


@router.get("/")
async def root():
    return FileResponse("static/index.html")


@router.get("/api/sessions")
async def get_sessions():
    return {"sessions": list_sessions()}


@router.post("/api/sessions")
async def create_session():
    tid = uuid.uuid4().hex[:8]
    return {"thread_id": tid}


@router.post("/api/chat")
async def chat(req: ChatRequest, request: Request):
    thread_id = req.thread_id or uuid.uuid4().hex[:8]

    async def event_generator() -> AsyncGenerator[dict, None]:
        input_msg = req.message
        if req.preferences:
            input_msg = (
                f"用户偏好设置：{json.dumps(req.preferences, ensure_ascii=False)}\n\n"
                f"用户消息：{req.message}"
            )

        async for event in request.app.state.agent_app.astream(
            {"messages": [("user", input_msg)]},
            config={
                "configurable": {"thread_id": thread_id},
                "recursion_limit": 30,
            },
            stream_mode="updates",
        ):
            for node_name, node_output in event.items():
                if node_output is None:
                    continue
                msgs = node_output.get("messages", [])
                for msg in msgs:
                    if (
                        hasattr(msg, "type") and msg.type == "ai"
                        and not getattr(msg, "tool_calls", None)
                        and hasattr(msg, "content") and msg.content
                    ):
                        if isinstance(msg.content, str):
                            yield {"event": "token", "data": json.dumps({"text": msg.content}, ensure_ascii=False)}
                        elif isinstance(msg.content, list):
                            for block in msg.content:
                                if isinstance(block, dict) and block.get("type") == "text":
                                    yield {"event": "token", "data": json.dumps({"text": block["text"]}, ensure_ascii=False)}

                    tool_calls = getattr(msg, "tool_calls", None) or []
                    for tc in tool_calls:
                        yield {
                            "event": "tool_start",
                            "data": json.dumps({"tool": tc.get("name", ""), "args": tc.get("args", {})}, ensure_ascii=False),
                        }

                    if hasattr(msg, "type") and msg.type == "tool":
                        content = msg.content if hasattr(msg, "content") else str(msg)
                        try:
                            data = json.loads(content) if isinstance(content, str) else content
                            yield {
                                "event": "route",
                                "data": json.dumps(data, ensure_ascii=False),
                            }
                        except (json.JSONDecodeError, TypeError):
                            yield {
                                "event": "tool_result",
                                "data": json.dumps({"content": str(content)[:500]}, ensure_ascii=False),
                            }

        yield {"event": "done", "data": json.dumps({"thread_id": thread_id})}

    return EventSourceResponse(event_generator())


@router.post("/api/route/plan")
async def plan_route(req: RoutePlanRequest, request: Request):
    thread_id = req.thread_id or uuid.uuid4().hex[:8]

    prompt_parts = [
        f"请规划从「{req.origin}」到「{req.destination}」的骑行路线。",
    ]
    if req.waypoints:
        prompt_parts.append(f"途经点：{'、'.join(req.waypoints)}。")
    if req.avoid_highway:
        prompt_parts.append("请避开高速路段。")
    if req.prefer_greenway:
        prompt_parts.append("请优先选择绿道。")

    async def event_generator():
        async for event in request.app.state.agent_app.astream(
            {"messages": [("user", "\n".join(prompt_parts))]},
            config={
                "configurable": {"thread_id": thread_id},
                "recursion_limit": 30,
            },
            stream_mode="updates",
        ):
            for node_name, node_output in event.items():
                if node_output is None:
                    continue
                msgs = node_output.get("messages", [])
                for msg in msgs:
                    if (
                        hasattr(msg, "type") and msg.type == "ai"
                        and not getattr(msg, "tool_calls", None)
                        and hasattr(msg, "content") and msg.content
                    ):
                        if isinstance(msg.content, str):
                            yield {"event": "token", "data": json.dumps({"text": msg.content}, ensure_ascii=False)}
                    elif hasattr(msg, "type") and msg.type == "tool":
                        content = msg.content if hasattr(msg, "content") else str(msg)
                        try:
                            data = json.loads(content) if isinstance(content, str) else content
                            yield {"event": "route", "data": json.dumps(data, ensure_ascii=False)}
                        except (json.JSONDecodeError, TypeError):
                            pass
        yield {"event": "done", "data": json.dumps({"thread_id": thread_id})}

    return EventSourceResponse(event_generator())
