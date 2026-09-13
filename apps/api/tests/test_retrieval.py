import pytest

from app.retrieval.base import RetrievalScope
from app.retrieval.in_memory import InMemoryRetriever
from app.retrieval.seed import SEEDED_CHUNKS


@pytest.mark.asyncio
async def test_retrieval_filters_tenant_before_ranking() -> None:
    retriever = InMemoryRetriever(SEEDED_CHUNKS)

    results = await retriever.search(
        "evaluation regression datasets",
        RetrievalScope(tenant_id="tenant-demo", user_id="user-demo"),
        limit=5,
    )

    assert results
    assert all(item.tenant_id == "tenant-demo" for item in results)
    assert results[0].document_id == "eval-guide"


@pytest.mark.asyncio
async def test_retrieval_excludes_user_restricted_chunk() -> None:
    retriever = InMemoryRetriever(SEEDED_CHUNKS)

    results = await retriever.search(
        "confidential deployment controls",
        RetrievalScope(tenant_id="tenant-demo", user_id="user-demo"),
        limit=10,
    )

    assert all(item.document_id != "restricted-ops" for item in results)
