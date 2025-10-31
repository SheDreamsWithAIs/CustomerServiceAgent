"""
LangChain Version: v1.0+
Documentation Reference:
  - https://docs.langchain.com/oss/python/langchain/middleware
Last Verified: 2025-10-30
"""

from typing import List

from langchain.agents.middleware import dynamic_prompt, SummarizationMiddleware, ModelRequest


@dynamic_prompt
def concise_prompt(request: ModelRequest) -> str:
    """Adjust prompt for longer conversations to be more concise."""
    message_count = len(request.messages or [])
    base = "You are a helpful assistant."
    if message_count > 10:
        base += " Be concise and summarize when appropriate."
    return base


def get_default_middleware() -> List[object]:
    """Default middleware stack: summarization + dynamic prompt."""
    return [
        SummarizationMiddleware(
            model="openai:gpt-4o-mini",
            max_tokens_before_summary=4000,
            messages_to_keep=20,
        ),
        concise_prompt,
    ]


