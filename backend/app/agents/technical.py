"""
LangChain Version: v1.0+
Documentation Reference:
  - https://docs.langchain.com/oss/python/langchain/agents
  - https://docs.langchain.com/oss/python/langchain/retrieval
Last Verified: 2025-10-30
"""

from typing import Any, Dict, List
import logging

from langchain.agents import create_agent

from app.tools.search_documents import search_documents


def get_technical_support_agent():
    """Create the Technical Support agent (Pure RAG, two-step)."""
    system_prompt = (
        "You are a technical support specialist. "
        "CRITICAL: Always call the search_documents tool first to retrieve relevant context. "
        "Cite which retrieved passages you used. If no results are found, explain limitations and suggest escalation."
    )

    agent = create_agent(
        model="openai:gpt-4o-mini",
        tools=[search_documents],
        system_prompt=system_prompt,
        name="technical_support_agent",
    )
    return agent


def invoke_technical_agent(user_message: str) -> str:
    """Invoke the technical support agent and return final assistant text.

    Exceptions are logged and re-raised so the API can return HTTP 500.
    """
    logger = logging.getLogger("app.agents.technical")
    agent = get_technical_support_agent()
    try:
        result: Any = agent.invoke({
            "messages": [
                {"role": "user", "content": user_message}
            ]
        })
    except Exception as exc:
        logger.exception("Technical agent invocation failed")
        raise

    # Debug log the raw result type for troubleshooting
    logger.debug("Agent result type=%s value=%r", type(result), result)

    # Handle common shapes
    # 1) Dict with 'messages' (LangGraph-style)
    if isinstance(result, dict):
        # Log available keys for debugging
        logger.debug("Agent result keys: %s", list(result.keys()))
        if "messages" in result:
            messages = result.get("messages", [])  # type: ignore[assignment]
            if isinstance(messages, list) and messages:
                last = messages[-1]
                if isinstance(last, dict) and "content" in last:
                    return str(last.get("content", ""))
                # If using message objects, try attribute access
                if hasattr(last, "content"):
                    return str(getattr(last, "content"))
        # 1b) OpenAI ChatCompletion style: {'choices': [{'message': {'content': ...}}]}
        if "choices" in result:
            try:
                choices = result.get("choices")  # type: ignore[assignment]
                if isinstance(choices, list) and choices:
                    message = choices[-1].get("message") if isinstance(choices[-1], dict) else None
                    if isinstance(message, dict) and "content" in message:
                        return str(message.get("content", ""))
            except Exception:
                logger.exception("Failed to parse content from 'choices'")
        # 2) Dict with 'output'
        if "output" in result:
            return str(result.get("output", ""))
        # 3) Dict with 'content'
        if "content" in result:
            return str(result.get("content", ""))

    # 4) List of messages
    if isinstance(result, list) and result:
        last = result[-1]
        if isinstance(last, dict) and "content" in last:
            return str(last.get("content", ""))
        if hasattr(last, "content"):
            return str(getattr(last, "content"))

    # 5) A single message-like object
    if hasattr(result, "content"):
        return str(getattr(result, "content"))

    # 6) Plain string
    if isinstance(result, str):
        return result

    # Fallback: stringify safely
    logger.warning("Unrecognized agent result shape; stringifying result")
    return str(result)


