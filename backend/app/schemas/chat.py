from typing import Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., description="The user's message.")
    user_id: Optional[str] = Field(None, description="Unique user identifier.")
    thread_id: Optional[str] = Field(None, description="Conversation thread identifier.")


class BillingDetails(BaseModel):
    plan: Optional[str] = Field(None)
    balance_due: Optional[float] = Field(None)
    currency: Optional[str] = Field(None)
    last_invoice_id: Optional[str] = Field(None)
    open_tickets: Optional[int] = Field(None)
    policy_summary: Optional[str] = Field(None, description="Short policy snippet used to answer.")

class ChatResponse(BaseModel):
    message: str = Field(..., description="Assistant response.")
    route: Optional[str] = Field(None, description="Route/agent used for the response.")
    error: Optional[str] = Field(None, description="Optional error description when a failure occurs.")
    billing: Optional[BillingDetails] = Field(None, description="Structured billing details when available.")


