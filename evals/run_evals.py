import asyncio
import json
from pathlib import Path

from app.agents.graph import build_graph
from app.retrieval.in_memory import InMemoryRetriever
from app.retrieval.seed import SEEDED_CHUNKS
from scorers import score_case

DATASET = Path(__file__).with_name("dataset.jsonl")


async def run() -> int:
    graph = build_graph(InMemoryRetriever(SEEDED_CHUNKS))
    failures = 0
    for line in DATASET.read_text(encoding="utf-8").splitlines():
        case = json.loads(line)
        result = await graph.ainvoke(
            {
                "message": case["message"],
                "tenant_id": case["tenant_id"],
                "user_id": case["user_id"],
            }
        )
        score = score_case(
            answer=result["answer"],
            citation_ids=[citation.id for citation in result["citations"]],
            unsupported=result["unsupported"],
            expected_citation_ids=case["expected_citation_ids"],
            required_terms=case["required_terms"],
            expected_unsupported=case["expected_unsupported"],
        )
        status = "PASS" if score.passed else "FAIL"
        print(f"{status} {case['id']}")
        for failure in score.failures:
            print(f"  - {failure}")
        failures += int(not score.passed)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(run()))
