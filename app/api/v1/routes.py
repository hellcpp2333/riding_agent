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


def _parse_tool_result(content) -> list[dict]:
    """Parse tool result content into SSE events (route, tool_result, elevation)."""
    events: list[dict] = []
    try:
        if isinstance(content, str):
            route_part = content.split('\n\n[ELEVATION_JSON]')[0]
            json_str = route_part.split('\n\n[高程数据]')[0]
            data_parsed = json.loads(json_str)
        else:
            data_parsed = content
        events.append({"event": "route", "data": json.dumps(data_parsed, ensure_ascii=False)})
    except (json.JSONDecodeError, TypeError):
        events.append({
            "event": "tool_result",
            "data": json.dumps({"content": str(content)[:500]}, ensure_ascii=False),
        })

    if isinstance(content, str) and '[ELEVATION_JSON]' in content:
        try:
            elev_block = content.split('[ELEVATION_JSON]\n', 1)[1].strip()
            elev_data = json.loads(elev_block)
            events.append({"event": "elevation", "data": json.dumps(elev_data, ensure_ascii=False)})
        except (json.JSONDecodeError, IndexError):
            pass
    return events


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

        seen_tc_ids: set[str] = set()

        async for event in request.app.state.agent_app.astream_events(
            {"messages": [("user", input_msg)]},
            config={
                "configurable": {"thread_id": thread_id},
                "recursion_limit": 30,
            },
            version="v2",
        ):
            kind = event["event"]

            if kind == "on_chat_model_stream":
                chunk = event["data"]["chunk"]
                if chunk.content:
                    text = (
                        chunk.content if isinstance(chunk.content, str)
                        else "".join(
                            b.get("text", "") for b in chunk.content
                            if isinstance(b, dict) and b.get("type") == "text"
                        )
                    )
                    if text:
                        yield {"event": "token", "data": json.dumps({"text": text}, ensure_ascii=False)}

            elif kind == "on_chat_model_end":
                output = event["data"]["output"]
                for tc in output.tool_calls or []:
                    tc_id = tc.get("id", "")
                    if tc.get("name") and tc.get("args") and tc_id not in seen_tc_ids:
                        seen_tc_ids.add(tc_id)
                        yield {
                            "event": "tool_start",
                            "data": json.dumps({"tool": tc["name"], "args": tc["args"]}, ensure_ascii=False),
                        }

            elif kind == "on_chain_end" and event["name"] == "tools":
                output = event["data"]["output"]
                messages = output.get("messages", [])
                for msg in messages:
                    content = msg.content if hasattr(msg, "content") else str(msg)
                    for evt in _parse_tool_result(content):
                        yield evt

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
        seen_tc_ids: set[str] = set()

        async for event in request.app.state.agent_app.astream_events(
            {"messages": [("user", "\n".join(prompt_parts))]},
            config={
                "configurable": {"thread_id": thread_id},
                "recursion_limit": 30,
            },
            version="v2",
        ):
            kind = event["event"]

            if kind == "on_chat_model_stream":
                chunk = event["data"]["chunk"]
                if chunk.content:
                    text = (
                        chunk.content if isinstance(chunk.content, str)
                        else "".join(
                            b.get("text", "") for b in chunk.content
                            if isinstance(b, dict) and b.get("type") == "text"
                        )
                    )
                    if text:
                        yield {"event": "token", "data": json.dumps({"text": text}, ensure_ascii=False)}

            elif kind == "on_chat_model_end":
                output = event["data"]["output"]
                for tc in output.tool_calls or []:
                    tc_id = tc.get("id", "")
                    if tc.get("name") and tc.get("args") and tc_id not in seen_tc_ids:
                        seen_tc_ids.add(tc_id)
                        yield {
                            "event": "tool_start",
                            "data": json.dumps({"tool": tc["name"], "args": tc["args"]}, ensure_ascii=False),
                        }

            elif kind == "on_chain_end" and event["name"] == "tools":
                output = event["data"]["output"]
                messages = output.get("messages", [])
                for msg in messages:
                    content = msg.content if hasattr(msg, "content") else str(msg)
                    for evt in _parse_tool_result(content):
                        yield evt

        yield {"event": "done", "data": json.dumps({"thread_id": thread_id})}

    return EventSourceResponse(event_generator())