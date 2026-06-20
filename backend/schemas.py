from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    message: str
    sessionId: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    sessionId: str