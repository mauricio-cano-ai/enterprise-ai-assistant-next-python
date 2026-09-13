from typing import Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    conversation_id: str | None = None
    tenant_id: str = Field(min_length=1, max_length=100)
    user_id: str = Field(min_length=1, max_length=100)


class Citation(BaseModel):
    id: str
    title: str
    snippet: str
    source_url: str | None = None
    section: str | None = None


class RetrievedChunk(BaseModel):
    id: str
    document_id: str
    title: str
    text: str
    tenant_id: str
    allowed_user_ids: frozenset[str] = frozenset()
    source_url: str | None = None
    section: str | None = None
    score: float = 0.0


class TokenEvent(BaseModel):
    type: Literal["token"] = "token"
    text: str


class CitationEvent(BaseModel):
    type: Literal["citation"] = "citation"
    citation: Citation


class ErrorEvent(BaseModel):
    type: Literal["error"] = "error"
    message: str


class DoneEvent(BaseModel):
    type: Literal["done"] = "done"
