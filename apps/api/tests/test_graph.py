import pytest

from app.agents.graph import build_graph
from app.retrieval.in_memory import InMemoryRetriever
from app.retrieval.seed import SEEDED_CHUNKS


@pytest.mark.asyncio
async def test_graph_returns_grounded_answer_with_citation() -> None:
    graph = build_graph(InMemoryRetriever(SEEDED_CHUNKS))

    result = await graph.ainvoke(
        {
            "message": "How should production agent changes be evaluated?",
            "tenant_id": "tenant-demo",
            "user_id": "user-demo",
        }
    )

    assert result["unsupported"] is False
    assert "golden dataset" in result["answer"].lower()
    assert result["citations"][0].id == "eval-guide"


@pytest.mark.asyncio
async def test_graph_refuses_unsupported_question() -> None:
    graph = build_graph(InMemoryRetriever(SEEDED_CHUNKS))

    result = await graph.ainvoke(
        {
            "message": "What is the cafeteria menu tomorrow?",
            "tenant_id": "tenant-demo",
            "user_id": "user-demo",
        }
    )

    assert result["unsupported"] is True
    assert "knowledge base" in result["answer"].lower()
    assert result["citations"] == []
