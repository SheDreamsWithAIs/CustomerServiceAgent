from fastapi import APIRouter, Query
from fastapi import HTTPException

from app.schemas.chat import ChatRequest, ChatResponse, BillingDetails
from app.agents.technical import invoke_technical_agent
from app.core.config import get_settings
from app.agents.policy import invoke_policy_agent
from app.agents.billing import invoke_billing_agent
from app.agents.supervisor import invoke_supervisor
from app.tools.billing_accounts import lookup_account
from app.retrieval.retriever import similarity_search


router = APIRouter(tags=["chat"], prefix="/chat")


def _classify_intent(message: str) -> str:
    """Lightweight heuristic intent classifier for default routing.
    Returns one of: 'billing', 'policy', 'tech', 'unknown'.
    """
    m = (message or "").lower()
    # Billing cues
    billing_kw = [
        "billing", "invoice", "plan", "balance", "payment", "price", "refund",
        "charge", "subscription", "cancel", "downgrade", "upgrade",
    ]
    if any(k in m for k in billing_kw):
        return "billing"
    # Policy cues (e.g., "email policy", "terms", "privacy", "compliance")
    policy_kw = [
        "policy", "policies", "terms", "privacy", "compliance", "acceptable use",
        "email policy", "reply all", "gdpr",
    ]
    # handle missing space variant like "emailpolicy"
    # Prefer tech if asking about settings/navigation even if 'privacy' appears
    if (any(k in m for k in policy_kw) or "emailpolicy" in m) and ("settings" not in m):
        return "policy"
    # Tech support cues
    tech_kw = [
        "error", "bug", "issue", "fail", "install", "login", "timeout", "server",
        "api", "endpoint", "deploy", "integration", "troubleshoot",
    ]
    if any(k in m for k in tech_kw):
        return "tech"
    # UI/Settings navigation often implies technical help
    if "settings" in m or "where can i find" in m:
        return "tech"
    return "unknown"


@router.post("", response_model=ChatResponse, summary="Chat with the assistant")
def chat(request: ChatRequest, mode: str | None = Query(default=None, description="Optional routing override")) -> ChatResponse:
    """Chat endpoint supporting mode overrides; defaults to mocked echo for now."""
    settings = get_settings()
    try:
        # Normalize mode aliases
        if mode in {"tech_support", "technical", "tech"}:
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
        # Default: supervisor-only routing (heuristics disabled)
        content = request.message
        if request.user_id:
            content = f"[user_selector={request.user_id}] {content}"
        answer = invoke_supervisor(content)
        return ChatResponse(message=answer, route="supervisor")
    except Exception as exc:
        # Provide limited error details unless DEBUG is enabled
        detail = str(exc) if settings.debug else "Chat processing error"
        raise HTTPException(status_code=500, detail=detail) from exc


