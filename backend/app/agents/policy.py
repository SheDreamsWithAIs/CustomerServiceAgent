"""
LangChain Version: v1.0+
Documentation Reference:
  - https://docs.langchain.com/oss/python/langchain/agents
  - https://docs.langchain.com/oss/python/langchain/context-engineering
Last Verified: 2025-10-30
"""

from pathlib import Path
from typing import Any, Dict
import logging
import os

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from app.middleware.common import get_default_middleware


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _policy_path() -> Path:
    raw = os.getenv("POLICY_PATH", str(_repo_root() / "backend" / "policy" / "policy.md"))
    p = Path(raw)
    if not p.is_absolute():
        p = _repo_root() / raw
    return p


def _read_policy_text() -> str:
    path = _policy_path()
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return (
            "Policy snapshot not found. Please set POLICY_PATH or create backend/policy/policy.md."
        )


def get_policy_agent():
    policy_text = _read_policy_text()
    system_prompt = (
        "You are a policy & compliance specialist. "
        "Use ONLY the following policy snapshot as your source of truth. "
        "If a question is outside policy or not covered, say you cannot answer based on current policy.\n\n"
        f"Policy Snapshot:\n{policy_text}"
    )
    agent = create_agent(
        model="openai:gpt-4o-mini",
        tools=[],
        system_prompt=system_prompt,
        name="policy_agent",
        middleware=get_default_middleware(),
        checkpointer=InMemorySaver(),
    )
    return agent


def invoke_policy_agent(user_message: str, thread_id: str | None = None) -> str:
    logger = logging.getLogger("app.agents.policy")
    agent = get_policy_agent()
    result: Dict[str, Any] = agent.invoke(
        {"messages": [{"role": "user", "content": user_message}]},
        config={"configurable": {"thread_id": thread_id or "default"}},
    )
    logger.debug("Policy agent result type=%s", type(result))
    if isinstance(result, dict) and "messages" in result:
        messages = result.get("messages", [])
        if messages:
            last = messages[-1]
            if isinstance(last, dict) and "content" in last:
                return str(last.get("content", ""))
            if hasattr(last, "content"):
                return str(getattr(last, "content"))
    if isinstance(result, dict) and "choices" in result:
        choices = result.get("choices")
        if isinstance(choices, list) and choices:
            msg = choices[-1].get("message") if isinstance(choices[-1], dict) else None
            if isinstance(msg, dict) and "content" in msg:
                return str(msg.get("content", ""))
    if hasattr(result, "content"):
        return str(getattr(result, "content"))
    if isinstance(result, str):
        return result
    return str(result)


