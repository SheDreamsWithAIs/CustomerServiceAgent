"""
LangChain Version: v1.0+
Documentation Reference:
  - https://docs.langchain.com/oss/python/langchain/agents
  - https://docs.langchain.com/oss/python/langchain/retrieval
Last Verified: 2025-10-30
"""

from typing import Any, Dict
import json
import re

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from app.middleware.common import get_default_middleware

from app.tools.search_documents import search_documents
from app.tools.billing_accounts import get_account_info


def get_billing_agent():
    """Hybrid Billing agent: use account context (CAG) + retrieval (RAG)."""
    system_prompt = (
        "You are a billing specialist. "
        "Personalize answers using account data by calling get_account_info when a user_id/email is known. "
        "For policy or documentation details, call search_documents to retrieve relevant billing information before answering. "
        "If account data is missing, ask for user_id or email."
    )

    agent = create_agent(
        model="openai:gpt-4o-mini",
        tools=[get_account_info, search_documents],
        system_prompt=system_prompt,
        name="billing_agent",
        middleware=get_default_middleware(),
        checkpointer=InMemorySaver(),
    )
    return agent


def invoke_billing_agent(user_message: str, user_selector: str | None = None, thread_id: str | None = None) -> str:
    """Invoke billing agent. If user_selector is provided, include a hint to call get_account_info."""
    agent = get_billing_agent()
    content = user_message
    # If selector not explicitly provided, try to parse a prefix like [user_selector=...] from the message.
    if not user_selector:
        m = re.match(r"\[user_selector=([^\]]+)\]\s*(.*)", user_message)
        if m:
            user_selector = m.group(1).strip()
            content = m.group(2)
    if user_selector:
        content = f"[user_selector={user_selector}] {content}"
    result: Dict[str, Any] = agent.invoke(
        {"messages": [{"role": "user", "content": content}]},
        config={"configurable": {"thread_id": thread_id or "default"}},
    )
    if isinstance(result, dict):
        messages = result.get("messages", [])
        if messages:
            last = messages[-1]
            if isinstance(last, dict) and "content" in last:
                return str(last.get("content", ""))
            if hasattr(last, "content"):
                return str(getattr(last, "content"))
        if "choices" in result:
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


