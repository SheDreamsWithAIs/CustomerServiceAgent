from fastapi import APIRouter, Query
from fastapi import HTTPException

from app.schemas.chat import ChatRequest, ChatResponse, BillingDetails
from app.agents.technical import invoke_technical_agent
from app.core.config import get_settings
from app.agents.policy import invoke_policy_agent
from app.agents.billing import invoke_billing_agent
from app.tools.billing_accounts import lookup_account
from app.retrieval.retriever import similarity_search


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
        if mode == "billing":
            # Pass user_id if available as selector hint for personalization
            selector = request.user_id or None
            answer = invoke_billing_agent(request.message, user_selector=selector)

            billing_details = None
            if selector:
                acct = lookup_account(selector)
                if acct:
                    # Try to fetch a short policy snippet via retrieval (best-effort)
                    snippet = None
                    try:
                        hits = similarity_search("billing policy", k=1)
                        if hits:
                            text = hits[0].page_content or ""
                            snippet = text[:300]
                    except Exception:
                        snippet = None

                    billing_details = BillingDetails(
                        plan=acct.get("plan"),
                        balance_due=acct.get("balance_due"),
                        currency=acct.get("currency"),
                        last_invoice_id=acct.get("last_invoice_id"),
                        open_tickets=acct.get("open_tickets"),
                        policy_summary=snippet,
                    )

            return ChatResponse(message=answer, route="billing", error=None).model_copy(update={"billing": billing_details})
        return ChatResponse(message=f"echo: {request.message}", route="echo")
    except Exception as exc:
        # Provide limited error details unless DEBUG is enabled
        detail = str(exc) if settings.debug else "Chat processing error"
        raise HTTPException(status_code=500, detail=detail) from exc


