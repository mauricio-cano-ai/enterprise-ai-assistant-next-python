from dataclasses import dataclass
from typing import Protocol

from app.models.chat import RetrievedChunk


@dataclass(frozen=True)
class RetrievalScope:
    tenant_id: str
    user_id: str


class Retriever(Protocol):
    async def search(
        self,
        query: str,
        scope: RetrievalScope,
        limit: int = 5,
    ) -> list[RetrievedChunk]: ...
