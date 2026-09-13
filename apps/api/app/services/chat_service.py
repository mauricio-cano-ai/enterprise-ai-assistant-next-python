import asyncio
import json
from collections.abc import AsyncIterator

from app.models.chat import ChatRequest, CitationEvent, DoneEvent, ErrorEvent, TokenEvent


def _line(payload: dict) -> bytes:
    return (json.dumps(payload, separators=(",", ":")) + "\n").encode("utf-8")


def _token_chunks(answer: str) -> list[str]:
    words = answer.split(" ")
    return [word + (" " if index < len(words) - 1 else "") for index, word in enumerate(words)]


async def stream_chat(request: ChatRequest, graph) -> AsyncIterator[bytes]:
    try:
        result = await graph.ainvoke(
            {
                "message": request.message,
                "tenant_id": request.tenant_id,
                "user_id": request.user_id,
            }
        )
        for token in _token_chunks(result["answer"]):
            yield _line(TokenEvent(text=token).model_dump())
            await asyncio.sleep(0.015)
        for citation in result["citations"]:
            yield _line(CitationEvent(citation=citation).model_dump())
        yield _line(DoneEvent().model_dump())
    except Exception:
        yield _line(
            ErrorEvent(message="The assistant could not complete this request.").model_dump()
        )
