"""
LangChain Version: v1.0+
Documentation Reference:
  - https://docs.langchain.com/oss/python/langchain/agents
  - https://docs.langchain.com/oss/python/langchain/multi-agent
Last Verified: 2025-10-30
"""

from typing import Any, Dict

from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from app.middleware.common import get_default_middleware

from app.agents.technical import invoke_technical_agent
from app.agents.policy import invoke_policy_agent
from app.agents.billing import invoke_billing_agent


@tool
def tech_support(request: str) -> str:
    """Use for app usage, UI navigation (e.g., Settings paths), troubleshooting, errors, or APIs (RAG-backed)."""
    return invoke_technical_agent(request)


@tool
def policy_answer(request: str) -> str:
    """Use for policies, rules, governance, compliance, or terms (CAG-only; refuse outside snapshot)."""
    return invoke_policy_agent(request)


@tool
def billing_answer(request: str) -> str:
    """Use for billing/account topics (plan, invoices, payments). Keep [user_selector=...] prefix for personalization."""
    return invoke_billing_agent(request)


def get_supervisor_agent():
    system_prompt = (
        "You are the supervisor router. Choose exactly ONE tool per user message.\n"
        "Routing rules (priority order):\n"
        "1) If the question is about policies/rules/governance/terms, choose policy_answer.\n"
        "2) If the question is about app usage, UI navigation (e.g., 'Settings > Privacy'), troubleshooting, errors, or APIs, choose tech_support.\n"
        "3) If the topic is billing/account (plan, invoices, payments, refunds), choose billing_answer.\n"
        "Ambiguous cases: prefer policy when the user asks about 'policy/policies/terms/compliance', even if phrased as 'where can I find'.\n"
        "Personalization (CRITICAL): If the user message contains [user_selector=...], you MUST include that exact prefix AT THE BEGINNING of the billing_answer tool input, unchanged. Do NOT paraphrase or drop it.\n"
        "Return only the final answer to the user, not tool traces.\n\n"
        "Examples:\n"
        "- 'Where can I find data privacy settings?' -> tech_support\n"
        "- 'What is the email policy?' -> policy_answer\n"
        "- 'Where can I find the policies covering PTO?' -> policy_answer\n"
        "- '[user_selector=user_123] What is my balance and plan?' -> billing_answer\n"
    )
    agent = create_agent(
        model="openai:gpt-4o-mini",
        tools=[tech_support, policy_answer, billing_answer],
        system_prompt=system_prompt,
        name="supervisor",
        middleware=get_default_middleware(),
        checkpointer=InMemorySaver(),
    )
    return agent


def invoke_supervisor(user_message: str, thread_id: str | None = None) -> str:
    agent = get_supervisor_agent()
    result: Dict[str, Any] = agent.invoke(
        {"messages": [{"role": "user", "content": user_message}]},
        config={"configurable": {"thread_id": thread_id or "default"}},
    )
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


