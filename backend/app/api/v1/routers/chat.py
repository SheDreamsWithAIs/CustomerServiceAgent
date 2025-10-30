from fastapi import APIRouter, Query
from fastapi import HTTPException

from app.schemas.chat import ChatRequest, ChatResponse
from app.agents.technical import invoke_technical_agent
from app.core.config import get_settings
from app.agents.policy import invoke_policy_agent


router = APIRouter(tags=["chat"], prefix="/chat")


@router.post("", response_model=ChatResponse, summary="Chat with the assistant")
def chat(request: ChatRequest, mode: str | None = Query(default=None, description="Optional routing override")) -> ChatResponse:
    """Chat endpoint supporting mode overrides; defaults to mocked echo for now."""
    settings = get_settings()
    try:
        if mode == "tech_support":
            answer = invoke_technical_agent(request.message)
            return ChatResponse(message=answer, route="tech_support")
        if mode == "policy":
            answer = invoke_policy_agent(request.message)
            return ChatResponse(message=answer, route="policy")
        return ChatResponse(message=f"echo: {request.message}", route="echo")
    except Exception as exc:
        # Provide limited error details unless DEBUG is enabled
        detail = str(exc) if settings.debug else "Chat processing error"
        raise HTTPException(status_code=500, detail=detail) from exc


