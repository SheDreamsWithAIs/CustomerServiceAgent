from fastapi import APIRouter

from app.core.providers import list_enabled_providers, get_model_registry


router = APIRouter(tags=["providers"], prefix="/providers")


@router.get("", summary="List enabled AI providers")
def get_providers() -> dict:
    """Non-secret diagnostics of which providers are enabled and model aliases."""
    return {
        "enabled_providers": list_enabled_providers(),
        "model_registry": get_model_registry(),
    }


