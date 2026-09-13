import re

from app.models.chat import RetrievedChunk
from app.retrieval.base import RetrievalScope

_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
    "your",
}


def _terms(value: str) -> set[str]:
    return {term for term in re.findall(r"[a-z0-9]+", value.lower()) if term not in _STOPWORDS}


class InMemoryRetriever:
    def __init__(self, chunks: list[RetrievedChunk]) -> None:
        self._chunks = chunks

    async def search(
        self,
        query: str,
        scope: RetrievalScope,
        limit: int = 5,
    ) -> list[RetrievedChunk]:
        query_terms = _terms(query)
        eligible = [
            chunk
            for chunk in self._chunks
            if chunk.tenant_id == scope.tenant_id
            and (not chunk.allowed_user_ids or scope.user_id in chunk.allowed_user_ids)
        ]
        ranked: list[RetrievedChunk] = []
        for chunk in eligible:
            haystack = _terms(f"{chunk.title} {chunk.text} {chunk.section or ''}")
            overlap = len(query_terms & haystack)
            if overlap:
                ranked.append(chunk.model_copy(update={"score": float(overlap)}))
        ranked.sort(key=lambda item: (-item.score, item.document_id, item.id))

        if not ranked:
            return []

        best_score = ranked[0].score
        best_matches = [item for item in ranked if item.score == best_score]
        return best_matches[:limit]
