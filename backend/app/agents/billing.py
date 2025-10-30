"""
LangChain Version: v1.0+
Documentation Reference:
  - https://docs.langchain.com/oss/python/langchain/agents
  - https://docs.langchain.com/oss/python/langchain/retrieval
Last Verified: 2025-10-30
"""

from typing import Any, Dict
import json

from langchain.agents import create_agent

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
    )
    return agent


def invoke_billing_agent(user_message: str, user_selector: str | None = None) -> str:
    """Invoke billing agent. If user_selector is provided, include a hint to call get_account_info."""
    agent = get_billing_agent()
    content = user_message
    if user_selector:
        content = f"[user_selector={user_selector}] {user_message}"
    result: Dict[str, Any] = agent.invoke({
        "messages": [
            {"role": "user", "content": content}
        ]
    })
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


