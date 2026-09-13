from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.agents.graph import build_graph
from app.models.chat import ChatRequest
from app.retrieval.in_memory import InMemoryRetriever
from app.retrieval.seed import SEEDED_CHUNKS
from app.services.chat_service import stream_chat

router = APIRouter(prefix="/v1")
_retriever = InMemoryRetriever(SEEDED_CHUNKS)
_graph = build_graph(_retriever)

DEMO_ALLOWED_IDENTITIES = {
    ("tenant-demo", "user-demo"),
    ("tenant-demo", "security-admin"),
}


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest) -> StreamingResponse:
    if (request.tenant_id, request.user_id) not in DEMO_ALLOWED_IDENTITIES:
        raise HTTPException(status_code=403, detail="Retrieval scope is not authorized")
    return StreamingResponse(
        stream_chat(request, _graph),
        media_type="application/x-ndjson",
        headers={"Cache-Control": "no-store"},
    )
