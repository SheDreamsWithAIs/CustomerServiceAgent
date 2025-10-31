from fastapi import APIRouter, Query
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
import asyncio
import logging

from app.schemas.chat import ChatRequest, ChatResponse, BillingDetails
from app.agents.technical import invoke_technical_agent
from app.core.config import get_settings
from app.agents.policy import invoke_policy_agent
from app.agents.billing import invoke_billing_agent
from app.agents.supervisor import invoke_supervisor
from app.tools.billing_accounts import lookup_account
from app.retrieval.retriever import similarity_search


router = APIRouter(tags=["chat"], prefix="/chat")
logger = logging.getLogger("app.api.chat")


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


def _short_snippet(text: str, max_len: int = 220) -> str:
    """Return a concise one-paragraph snippet without dangling fragments."""
    if not text:
        return ""
    t = text.strip().replace("\r", "")
    if len(t) <= max_len:
        return t
    cut = t[:max_len]
    # prefer to cut at last period or newline within the window
    pos = max(cut.rfind("."), cut.rfind("\n"))
    if pos >= 40:  # avoid super-short truncations
        cut = cut[: pos + 1]
    return cut.rstrip() + " …"

@router.post("", response_model=ChatResponse, summary="Chat with the assistant")
def chat(request: ChatRequest, mode: str | None = Query(default=None, description="Optional routing override")) -> ChatResponse:
    """Chat endpoint supporting mode overrides; defaults to mocked echo for now."""
    settings = get_settings()
    try:
        # Normalize mode aliases
        if mode in {"tech_support", "technical", "tech"}:
            answer = invoke_technical_agent(request.message, thread_id=request.thread_id)
            logger.info("route=tech_support mode=%s thread=%s", mode, request.thread_id)
            return ChatResponse(message=answer, route="tech_support")
        if mode == "policy":
            answer = invoke_policy_agent(request.message, thread_id=request.thread_id)
            logger.info("route=policy mode=%s thread=%s", mode, request.thread_id)
            return ChatResponse(message=answer, route="policy")
        if mode == "billing":
            # Pass user_id if available as selector hint for personalization
            selector = request.user_id or None
            answer = invoke_billing_agent(request.message, user_selector=selector, thread_id=request.thread_id)

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
                            snippet = _short_snippet(text)
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

            logger.info("route=billing mode=%s thread=%s", mode, request.thread_id)
            return ChatResponse(message=answer, route="billing", error=None).model_copy(update={"billing": billing_details})
        # Deterministic billing guard: if user_id is present and billing-like terms appear, route to billing
        m = (request.message or "").lower()
        billing_kw = [
            "billing", "invoice", "plan", "balance", "payment", "price", "refund",
            "charge", "subscription", "cancel", "downgrade", "upgrade", "account",
        ]
        if request.user_id and any(k in m for k in billing_kw):
            selector = request.user_id
            answer = invoke_billing_agent(request.message, user_selector=selector, thread_id=request.thread_id)

            billing_details = None
            acct = lookup_account(selector)
            if acct:
                snippet = None
                try:
                    hits = similarity_search("billing policy", k=1)
                    if hits:
                        text = hits[0].page_content or ""
                        snippet = _short_snippet(text)
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
            logger.info("route=billing(guard) thread=%s", request.thread_id)
            return ChatResponse(message=answer, route="billing", error=None).model_copy(update={"billing": billing_details})

        # Default: supervisor-only routing (heuristics disabled)
        content = request.message
        if request.user_id:
            content = f"[user_selector={request.user_id}] {content}"
        answer = invoke_supervisor(content, thread_id=request.thread_id)
        logger.info("route=supervisor thread=%s", request.thread_id)
        return ChatResponse(message=answer, route="supervisor")
    except Exception as exc:
        # Provide limited error details unless DEBUG is enabled
        detail = str(exc) if settings.debug else "Chat processing error"
        raise HTTPException(status_code=500, detail=detail) from exc

@router.post("/stream", summary="Chat with streaming (text/event-stream)")
async def chat_stream(request: ChatRequest, mode: str | None = Query(default=None, description="Optional routing override")):
    """Stream the assistant's message as server-sent events. Structured fields not included in stream."""
    settings = get_settings()

    async def event_generator(text: str):
        # Simple character streaming for demo; can switch to token streaming later
        for ch in text:
            yield f"data: {ch}\n\n"
            await asyncio.sleep(0.008)
        yield "data: [DONE]\n\n"

    try:
        # Reuse same routing logic to get final text answer
        if mode in {"tech_support", "technical", "tech"}:
            answer = invoke_technical_agent(request.message, thread_id=request.thread_id)
            return StreamingResponse(event_generator(answer), media_type="text/event-stream")
        if mode == "policy":
            answer = invoke_policy_agent(request.message, thread_id=request.thread_id)
            return StreamingResponse(event_generator(answer), media_type="text/event-stream")
        if mode == "billing":
            selector = request.user_id or None
            answer = invoke_billing_agent(request.message, user_selector=selector, thread_id=request.thread_id)
            return StreamingResponse(event_generator(answer), media_type="text/event-stream")

        # Deterministic billing guard
        m = (request.message or "").lower()
        billing_kw = [
            "billing", "invoice", "plan", "balance", "payment", "price", "refund",
            "charge", "subscription", "cancel", "downgrade", "upgrade", "account",
        ]
        if request.user_id and any(k in m for k in billing_kw):
            answer = invoke_billing_agent(request.message, user_selector=request.user_id, thread_id=request.thread_id)
            return StreamingResponse(event_generator(answer), media_type="text/event-stream")

        # Supervisor default
        content = request.message
        if request.user_id:
            content = f"[user_selector={request.user_id}] {content}"
        answer = invoke_supervisor(content, thread_id=request.thread_id)
        return StreamingResponse(event_generator(answer), media_type="text/event-stream")
    except Exception as exc:
        detail = str(exc) if settings.debug else "Chat processing error"
        raise HTTPException(status_code=500, detail=detail) from exc


