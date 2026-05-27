import asyncio as _asyncio
import json
import os
from datetime import date
from typing import Annotated, Literal

from langchain.agents.middleware import SummarizationMiddleware
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.runtime import Runtime
from typing_extensions import TypedDict

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL")

BAIDU_MAPS_API_KEY = os.environ["BAIDU_MAPS_API_KEY"]
# NOTE: API key embedded in URL — avoid logging this URL in errors/traces
BAIDU_MCP_URL = f"https://mcp.map.baidu.com/mcp?ak={BAIDU_MAPS_API_KEY}"

LLM_TIMEOUT_S = 20

SYSTEM_PROMPT = (
    f"今天是 {date.today()}。"
    "你是一个专业的骑行路线规划助手。你可以帮助用户：\n"
    "1. 规划骑行路线：直接调用 map_directions 工具，传入中文地址名即可（无需先做地理编码）\n"
    "2. 搜索沿途设施：使用 map_search_places 在路线沿途搜索补给点、修车店、咖啡店等\n"
    "3. 查询天气：使用 map_weather 了解骑行当天的天气状况\n"
    "4. 地点查询：使用 map_geocode/map_reverse_geocode 查找特定地点\n"
    "5. 多路线对比：使用 map_directions_matrix 比较多个起终点的路线\n\n"
    "工作流程：\n"
    "- 用户提出路线规划时，直接用 map_directions(model='riding') 规划，"
    "起点终点直接传中文地址名，不需要先调用地理编码\n"
    "- 规划路线后，主动告知距离、预计时间，并询问是否需要搜索沿途设施\n"
    "- 如果用户要搜索沿途POI，使用 map_search_places 的 location 参数做周边搜索\n"
    "- 用中文回复，语气友好专业\n"
    "- 回答中涉及距离、时间等数据时，以工具返回的结果为准"
)

SUMMARY_PROMPT_ZH = """<role>
骑行对话上下文提取助手
</role>

<primary_objective>
从对话历史中提取关键信息，生成简洁摘要。
</primary_objective>

<instructions>
提取以下信息：

1. 用户的骑行偏好（避开高速、偏好绿道等）
2. 对话中已规划的路线（起点、终点、距离、时间）
3. 用户查询过的地点
4. 其他需要记住的关键信息

严格按以下格式输出：

## 用户偏好
## 已规划路线
## 已查询地点
## 其他信息
</instructions>

<messages>
{messages}
</messages>"""


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


class DebugSummarizationMiddleware(SummarizationMiddleware):
    def before_model(self, state, runtime):
        result = super().before_model(state, runtime)
        if result is not None:
            for msg in result.get("messages", []):
                if (
                    isinstance(msg, HumanMessage)
                    and msg.additional_kwargs.get("lc_source") == "summarization"
                ):
                    print(f"\n{'='*60}")
                    print("[记忆总结] 触发总结条件：")
                    print(msg.content)
                    print(f"{'='*60}\n")
        return result


def build_agent(checkpointer):
    llm = ChatOpenAI(
        model="glm-5v-turbo",
        temperature=0,
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
        timeout=LLM_TIMEOUT_S,
        extra_body={"thinking": {"type": "disabled"}},
    )

    summary_llm = ChatOpenAI(
        model="glm-5v-turbo",
        temperature=0,
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
        timeout=LLM_TIMEOUT_S,
        extra_body={"thinking": {"type": "disabled"}},
    )

    summarization = DebugSummarizationMiddleware(
        model=summary_llm,
        trigger=("messages", 15),
        keep=("messages", 6),
        summary_prompt=SUMMARY_PROMPT_ZH,
    )

    # Synchronous tool wrappers for MCP (LangGraph nodes are sync)
    def _mcp_call_tool_sync(tool_name: str, args: dict) -> str:
        async def _call():
            async with streamablehttp_client(BAIDU_MCP_URL) as (read, write, _):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await session.call_tool(tool_name, arguments=args)
                    texts = []
                    for block in result.content:
                        if hasattr(block, "text"):
                            texts.append(block.text)
                        elif isinstance(block, dict):
                            texts.append(json.dumps(block, ensure_ascii=False))
                        else:
                            texts.append(str(block))
                    return "\n".join(texts)
        try:
            return _asyncio.run(_call())
        except Exception as e:
            return json.dumps({"error": f"MCP调用失败: {str(e)}"}, ensure_ascii=False)

    @tool
    def map_directions(
        origin: str, destination: str, model: str = "riding"
    ) -> str:
        """规划骑行路线。origin 为起点位置名称或纬经度坐标(纬度,经度)，
        destination 为终点位置名称或纬经度坐标(纬度,经度)。
        model 为路线类型: riding(骑行,默认), driving(驾车), walking(步行), transit(公交)。
        可直接传中文地址名，无需先做地理编码。返回路线距离、耗时和步骤。"""
        return _mcp_call_tool_sync("map_directions", {
            "origin": origin,
            "destination": destination,
            "model": model,
        })

    @tool
    def map_geocode(address: str, city: str = "") -> str:
        """地理编码：将地址转换为经纬度坐标。address 为地址名称，city 为城市名(可选)。"""
        return _mcp_call_tool_sync("map_geocode", {
            "address": address,
            "city": city,
        })

    @tool
    def map_reverse_geocode(lat: float, lng: float) -> str:
        """逆地理编码：根据经纬度坐标获取地址描述和POI信息。
        lat 为纬度，lng 为经度 (bd09ll坐标系)。"""
        return _mcp_call_tool_sync("map_reverse_geocode", {
            "lat": lat,
            "lng": lng,
        })

    @tool
    def map_search_places(
        query: str, region: str = "", location: str = "", radius: int = 1000
    ) -> str:
        """搜索地点/POI。query 为搜索关键词(如'便利店'、'咖啡店')，
        region 为城市名(如'北京市')。
        location 为周边搜索中心点坐标(纬度,经度)，radius 为搜索半径(米, 默认1000)。
        如果需要对路线沿途或某个位置周边搜索，请使用 location 和 radius 参数。"""
        args: dict = {"query": query}
        if region:
            args["region"] = region
        if location:
            args["location"] = location
            args["radius"] = radius
        return _mcp_call_tool_sync("map_search_places", args)

    @tool
    def map_place_details(uid: str) -> str:
        """查询POI详情。uid 为POI的唯一标识(从地点搜索获取)。返回评分、营业时间等详情。"""
        return _mcp_call_tool_sync("map_place_details", {
            "uid": uid,
        })

    @tool
    def map_weather(location: str = "", district_id: str = "") -> str:
        """查询天气。location 为经纬度坐标(经度,纬度)，district_id 为6位行政区划代码。
        返回实时天气和未来5天天气预报。二者至少提供一个。"""
        args: dict = {}
        if location:
            args["location"] = location
        if district_id:
            args["district_id"] = district_id
        return _mcp_call_tool_sync("map_weather", args)

    @tool
    def map_directions_matrix(
        origins: str, destinations: str, model: str = "riding"
    ) -> str:
        """批量算路：计算多个起点到多个终点的距离和时间。
        origins 为多个起点坐标用|分隔(纬度,经度)，
        destinations 为多个终点坐标用|分隔(纬度,经度)。
        model 为路线类型: riding(骑行,默认), driving(驾车), walking(步行)。"""
        return _mcp_call_tool_sync("map_directions_matrix", {
            "origins": origins,
            "destinations": destinations,
            "model": model,
        })

    tools = [
        map_directions,
        map_geocode,
        map_reverse_geocode,
        map_search_places,
        map_place_details,
        map_weather,
        map_directions_matrix,
    ]
    llm_with_tools = llm.bind_tools(tools)

    # Graph nodes

    def summarize_node(state: AgentState) -> dict:
        messages = state["messages"]
        if messages and not isinstance(messages[-1], HumanMessage):
            return {}
        mw_result = summarization.before_model(state, Runtime())
        if mw_result:
            return dict(mw_result)
        return {}

    def agent_node(state: AgentState, config: RunnableConfig) -> dict:
        messages = [SystemMessage(content=SYSTEM_PROMPT)]
        messages.extend(state["messages"])
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    def tools_node(state: AgentState) -> dict:
        last_msg = state["messages"][-1]
        tool_messages = []
        for tc in last_msg.tool_calls:
            tool_name = tc["name"]
            tool_args = tc["args"]
            for t in tools:
                if t.name == tool_name:
                    result = t.invoke(tool_args)
                    tool_messages.append(ToolMessage(
                        content=str(result), tool_call_id=tc["id"],
                    ))
                    break
        return {"messages": tool_messages}

    def route_after_agent(state: AgentState) -> Literal["tools", "__end__"]:
        last_msg = state["messages"][-1]
        if getattr(last_msg, "tool_calls", None):
            return "tools"
        return "__end__"

    # Build graph

    builder = StateGraph(AgentState)
    builder.add_node("summarize", summarize_node)
    builder.add_node("agent", agent_node)
    builder.add_node("tools", tools_node)

    builder.add_edge(START, "summarize")
    builder.add_edge("summarize", "agent")
    builder.add_conditional_edges("agent", route_after_agent, {
        "tools": "tools",
        "__end__": END,
    })
    builder.add_edge("tools", "summarize")

    return builder.compile(checkpointer=checkpointer)
