from app.models.chat import Citation, RetrievedChunk

FALLBACK = (
    "I don't have enough authorized context in the demo knowledge base to answer that safely."
)


def compose_grounded_answer(chunks: list[RetrievedChunk]) -> tuple[str, list[Citation], bool]:
    if not chunks:
        return FALLBACK, [], True

    selected = chunks[:2]
    answer = " ".join(chunk.text for chunk in selected)
    citations = [
        Citation(
            id=chunk.document_id,
            title=chunk.title,
            snippet=chunk.text[:160],
            source_url=chunk.source_url,
            section=chunk.section,
        )
        for chunk in selected
    ]
    return answer, citations, False
