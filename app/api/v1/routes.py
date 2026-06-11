import json
import uuid
from typing import AsyncGenerator

from fastapi import APIRouter, Depends, Request
from sse_starlette.sse import EventSourceResponse

from app.api.v1.schemas import ChatRequest, RoutePlanRequest
from app.auth.dependencies import get_current_user
from app.db import list_sessions
from app.models import User

router = APIRouter()


@router.get("/api/sessions")
async def get_sessions(user: User = Depends(get_current_user)):
    return {"sessions": list_sessions()}


@router.post("/api/sessions")
async def create_session(user: User = Depends(get_current_user)):
    tid = uuid.uuid4().hex[:8]
    return {"thread_id": tid}


@router.post("/api/chat")
async def chat(
    req: ChatRequest,
    request: Request,
    user: User = Depends(get_current_user),
):
    thread_id = req.thread_id or uuid.uuid4().hex[:8]

    async def event_generator() -> AsyncGenerator[dict, None]:
        input_msg = req.message
        if req.preferences:
            input_msg = (
                f"{user.username}的偏好设置：{json.dumps(req.preferences, ensure_ascii=False)}\n\n"
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
                        text = ""
                        if isinstance(msg.content, str):
                            text = msg.content
                        elif isinstance(msg.content, list):
                            for block in msg.content:
                                if isinstance(block, dict) and block.get("type") == "text":
                                    text += block.get("text", "")
                        # Stream text character by character for real-time display
                        if text:
                            for ch in text:
                                yield {"event": "token", "data": json.dumps({"text": ch}, ensure_ascii=False)}

                    tool_calls = getattr(msg, "tool_calls", None) or []
                    for tc in tool_calls:
                        yield {
                            "event": "tool_start",
                            "data": json.dumps({"tool": tc.get("name", ""), "args": tc.get("args", {})}, ensure_ascii=False),
                        }

                    if hasattr(msg, "type") and msg.type == "tool":
                        content = msg.content if hasattr(msg, "content") else str(msg)
                        # 发送 route 事件（不含高程 JSON）
                        try:
                            if isinstance(content, str):
                                route_part = content.split('\n\n[ELEVATION_JSON]')[0]
                                json_str = route_part.split('\n\n[高程数据]')[0]
                                data_parsed = json.loads(json_str)
                            else:
                                data_parsed = content
                            yield {
                                "event": "route",
                                "data": json.dumps(data_parsed, ensure_ascii=False),
                            }
                        except (json.JSONDecodeError, TypeError):
                            yield {
                                "event": "tool_result",
                                "data": json.dumps({"content": str(content)[:500]}, ensure_ascii=False),
                            }
                        # 发送独立的 elevation 事件
                        if isinstance(content, str) and '[ELEVATION_JSON]' in content:
                            try:
                                elev_block = content.split('[ELEVATION_JSON]\n', 1)[1].strip()
                                elev_data = json.loads(elev_block)
                                yield {
                                    "event": "elevation",
                                    "data": json.dumps(elev_data, ensure_ascii=False),
                                }
                            except (json.JSONDecodeError, IndexError):
                                pass

        yield {"event": "done", "data": json.dumps({"thread_id": thread_id})}

    return EventSourceResponse(event_generator())


@router.post("/api/route/plan")
async def plan_route(
    req: RoutePlanRequest,
    request: Request,
    user: User = Depends(get_current_user),
):
    thread_id = req.thread_id or uuid.uuid4().hex[:8]

    prompt_parts = [
        f"请为{user.username}规划从「{req.origin}」到「{req.destination}」的骑行路线。",
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
                        text = msg.content if isinstance(msg.content, str) else ""
                        if text:
                            for ch in text:
                                yield {"event": "token", "data": json.dumps({"text": ch}, ensure_ascii=False)}
                    elif hasattr(msg, "type") and msg.type == "tool":
                        content = msg.content if hasattr(msg, "content") else str(msg)
                        try:
                            if isinstance(content, str):
                                route_part = content.split('\n\n[ELEVATION_JSON]')[0]
                                json_str = route_part.split('\n\n[高程数据]')[0]
                                data_parsed = json.loads(json_str)
                            else:
                                data_parsed = content
                            yield {"event": "route", "data": json.dumps(data_parsed, ensure_ascii=False)}
                        except (json.JSONDecodeError, TypeError):
                            pass
                        # 发送独立的 elevation 事件
                        if isinstance(content, str) and '[ELEVATION_JSON]' in content:
                            try:
                                elev_block = content.split('[ELEVATION_JSON]\n', 1)[1].strip()
                                elev_data = json.loads(elev_block)
                                yield {"event": "elevation", "data": json.dumps(elev_data, ensure_ascii=False)}
                            except (json.JSONDecodeError, IndexError):
                                pass
        yield {"event": "done", "data": json.dumps({"thread_id": thread_id})}

    return EventSourceResponse(event_generator())