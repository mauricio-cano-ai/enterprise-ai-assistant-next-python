from typing import TypedDict

from app.models.chat import Citation, RetrievedChunk


class AgentState(TypedDict, total=False):
    message: str
    tenant_id: str
    user_id: str
    chunks: list[RetrievedChunk]
    answer: str
    citations: list[Citation]
    unsupported: bool
