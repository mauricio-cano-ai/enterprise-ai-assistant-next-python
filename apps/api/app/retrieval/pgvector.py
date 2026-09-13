from app.models.chat import RetrievedChunk
from app.retrieval.base import RetrievalScope


class PgVectorRetriever:
    def __init__(self, database_url: str | None) -> None:
        if not database_url:
            raise ValueError("DATABASE_URL is required for pgvector retrieval")
        self._database_url = database_url

    async def search(
        self,
        query: str,
        scope: RetrievalScope,
        limit: int = 5,
    ) -> list[RetrievedChunk]:
        raise NotImplementedError(
            "PgVectorRetriever is a production adapter boundary; "
            "use RETRIEVAL_BACKEND=inmemory locally"
        )
