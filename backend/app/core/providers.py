import os
from typing import Dict, List


def list_enabled_providers() -> List[str]:
    """Return a list of enabled provider names (non-secret diagnostics)."""
    enabled: List[str] = []

    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    if openai_api_key:
        enabled.append("openai")

    bedrock_enabled = os.getenv("BEDROCK_ENABLED", "false").lower() in {"1", "true", "yes"}
    if bedrock_enabled:
        enabled.append("bedrock")

    return enabled


def get_model_registry() -> Dict[str, str]:
    """Return a simple model alias registry for logging/selection (no clients here)."""
    return {
        "openai_default": os.getenv("OPENAI_MODEL", "openai:gpt-4o-mini"),
        "bedrock_default": os.getenv("BEDROCK_MODEL", "bedrock:anthropic:haiku"),
    }


