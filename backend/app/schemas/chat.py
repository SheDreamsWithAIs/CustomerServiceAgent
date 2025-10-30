from typing import Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., description="The user's message.")
    user_id: Optional[str] = Field(None, description="Unique user identifier.")
    thread_id: Optional[str] = Field(None, description="Conversation thread identifier.")


class ChatResponse(BaseModel):
    message: str = Field(..., description="Assistant response.")
    route: Optional[str] = Field(None, description="Route/agent used for the response.")
    error: Optional[str] = Field(None, description="Optional error description when a failure occurs.")


