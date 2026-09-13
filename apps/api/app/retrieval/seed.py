from app.models.chat import RetrievedChunk

SEEDED_CHUNKS = [
    RetrievedChunk(
        id="eval-1",
        document_id="eval-guide",
        title="AI Evaluation Guide",
        text=(
            "Production agent changes should be compared against a representative golden "
            "dataset with deterministic checks, regression thresholds, and staged rollout."
        ),
        tenant_id="tenant-demo",
        source_url="https://example.local/evaluation-guide",
        section="Regression gates",
    ),
    RetrievedChunk(
        id="rag-1",
        document_id="retrieval-guide",
        title="Secure Retrieval Guide",
        text=(
            "Authorization filters must be applied before retrieved chunks become eligible "
            "for ranking or language-model context."
        ),
        tenant_id="tenant-demo",
        source_url="https://example.local/retrieval-guide",
        section="Authorization-aware retrieval",
    ),
    RetrievedChunk(
        id="stream-1",
        document_id="streaming-guide",
        title="Streaming Architecture Guide",
        text=(
            "A normal text-generation chat can use HTTP response streaming while persistent "
            "bidirectional media sessions may justify WebSockets."
        ),
        tenant_id="tenant-demo",
        source_url="https://example.local/streaming-guide",
        section="Protocol choice",
    ),
    RetrievedChunk(
        id="ops-secret",
        document_id="restricted-ops",
        title="Restricted Operations Notes",
        text="Confidential deployment controls for security administrators.",
        tenant_id="tenant-demo",
        allowed_user_ids=frozenset({"security-admin"}),
        section="Restricted",
    ),
    RetrievedChunk(
        id="other-tenant",
        document_id="other-tenant-doc",
        title="Other Tenant Handbook",
        text="Evaluation process belonging to another tenant.",
        tenant_id="tenant-other",
    ),
]
