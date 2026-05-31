import os
os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("LLM_MODEL", "test-model")
os.environ.setdefault("BAIDU_MAPS_API_KEY", "test-baidu-key")

import pytest
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

from app.agents.agent import _sanitize_messages, _trim_messages


def _tc_msg(id_: str, content: str = "") -> ToolMessage:
    return ToolMessage(content=content, tool_call_id=id_)


def _ai_msg(tool_calls: list[dict], content: str = "") -> AIMessage:
    return AIMessage(content=content, tool_calls=tool_calls)


def _tc(id_: str, name: str = "test_tool") -> dict:
    return {"name": name, "args": {}, "id": id_}


class TestSanitizeMessages:
    def test_empty_list(self):
        assert _sanitize_messages([]) == []

    def test_no_tool_messages(self):
        msgs = [HumanMessage(content="hello"), AIMessage(content="hi")]
        result = _sanitize_messages(msgs)
        assert len(result) == 2
        assert result == msgs

    def test_valid_tool_roundtrip(self):
        msgs = [
            HumanMessage(content="query"),
            _ai_msg([_tc("1")]),
            _tc_msg("1", "result"),
            AIMessage(content="done"),
        ]
        result = _sanitize_messages(msgs)
        assert len(result) == 4

    def test_orphaned_tool_message_removed(self):
        msgs = [
            HumanMessage(content="query"),
            _tc_msg("orphan", "no matching AI"),
            AIMessage(content="done"),
        ]
        result = _sanitize_messages(msgs)
        assert len(result) == 2
        assert not any(isinstance(m, ToolMessage) for m in result)

    def test_orphaned_tool_calls_removed(self):
        msgs = [
            HumanMessage(content="query"),
            _ai_msg([_tc("orphan")]),
            AIMessage(content="done"),
        ]
        result = _sanitize_messages(msgs)
        assert len(result) == 2
        assert isinstance(result[0], HumanMessage)
        assert isinstance(result[1], AIMessage)
        assert not getattr(result[1], "tool_calls", None)

    def test_partial_tool_calls_filtered(self):
        msgs = [
            HumanMessage(content="query"),
            _ai_msg([_tc("1"), _tc("orphan")]),
            _tc_msg("1", "result"),
            AIMessage(content="done"),
        ]
        result = _sanitize_messages(msgs)
        assert len(result) == 4
        ai = result[1]
        assert len(ai.tool_calls) == 1
        assert ai.tool_calls[0]["id"] == "1"

    def test_mixed_orphans(self):
        msgs = [
            HumanMessage(content="q1"),
            _ai_msg([_tc("1")]),
            _tc_msg("1", "ok"),
            _ai_msg([_tc("orphan_ai")]),
            _tc_msg("orphan_tool", "stray"),
            AIMessage(content="done"),
        ]
        result = _sanitize_messages(msgs)
        assert len(result) == 4
        ids = [type(m).__name__ for m in result]
        assert ids == ["HumanMessage", "AIMessage", "ToolMessage", "AIMessage"]

    def test_all_tool_messages_orphaned(self):
        msgs = [
            _tc_msg("1", "o1"),
            _tc_msg("2", "o2"),
            AIMessage(content="no tools here"),
        ]
        result = _sanitize_messages(msgs)
        assert len(result) == 1
        assert isinstance(result[0], AIMessage)

    def test_all_ai_tool_calls_orphaned(self):
        msgs = [
            _ai_msg([_tc("1")]),
            _ai_msg([_tc("2")]),
            AIMessage(content="done"),
        ]
        result = _sanitize_messages(msgs)
        assert len(result) == 1
        assert isinstance(result[0], AIMessage)
        assert not getattr(result[0], "tool_calls", None)

    def test_preserves_message_order(self):
        msgs = [
            HumanMessage(content="q1"),
            _ai_msg([_tc("1"), _tc("orphan")]),
            _tc_msg("1", "ok"),
            AIMessage(content="mid"),
            _ai_msg([_tc("2")]),
            _tc_msg("2", "ok2"),
            HumanMessage(content="q2"),
        ]
        result = _sanitize_messages(msgs)
        # _ai_msg with tc "1" and "orphan" gets filtered to just "1"
        assert len(result) == 7
        assert isinstance(result[0], HumanMessage)
        assert result[0].content == "q1"
        assert isinstance(result[-1], HumanMessage)
        assert result[-1].content == "q2"


class TestTrimMessagesWithSanitize:
    def test_sanitize_called_before_trim(self):
        msgs = [
            _ai_msg([_tc("orphan")]),
        ] + [HumanMessage(content=f"msg{i}") for i in range(30)]
        result = _trim_messages(msgs, max_count=10)
        assert len(result) <= 10
        assert not any(
            getattr(m, "tool_calls", None) for m in result
            if isinstance(m, AIMessage)
        )

    def test_sanitize_preserves_valid_messages(self):
        msgs = [
            HumanMessage(content="q"),
            _ai_msg([_tc("1")]),
            _tc_msg("1", "ok"),
            AIMessage(content="answer"),
        ]
        result = _trim_messages(msgs, max_count=10)
        assert len(result) == 4
