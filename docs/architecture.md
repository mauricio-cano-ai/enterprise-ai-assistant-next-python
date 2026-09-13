# Architecture

## Runtime path

```text
Browser
  -> Next.js App Router
  -> POST /api/chat Route Handler
  -> FastAPI POST /v1/chat/stream
  -> LangGraph workflow
  -> authorization-aware retriever
  -> deterministic grounded generator
  -> NDJSON token/citation/done events
```

The Next.js Route Handler acts as the browser-facing BFF and forwards the backend response body without waiting for the complete answer. The browser parses newline-delimited JSON incrementally and renders answer text plus citation-safe metadata.

## Rendering boundary

The application page and architecture content are Server Components. `ChatShell` is the client boundary because it owns browser-side stream state, cancellation, retry behavior, and event handling. Components imported beneath that boundary remain in the client subtree without forcing the entire page into the client bundle.

## Trust boundary

The browser receives only:

- answer text
- citation id
- document title
- short citation snippet
- optional source URL
- optional section label

Raw retrieval chunks, tenant/user authorization fields, ranking scores, embeddings, internal storage identifiers, and hidden prompts remain in the Python service.

Retrieval eligibility is filtered by `tenant_id` and `user_id` before lexical ranking. The seeded demo includes a restricted document that is invisible to the normal demo user and covered by tests/evaluations.

## Retrieval contract

The backend depends on a narrow asynchronous `Retriever` protocol rather than on the in-memory implementation directly. `InMemoryRetriever` powers the local keyless demo. `PgVectorRetriever` establishes the production adapter boundary and requires `DATABASE_URL`; a real database/vector implementation is intentionally not claimed as part of the MVP.

## Evaluation path

The deterministic evaluation path is:

```text
candidate change
  -> golden dataset
  -> graph execution
  -> citation / answer-term / unsupported checks
  -> pass or non-zero regression exit
```

Cases cover normal evaluation guidance, secure retrieval, streaming protocol selection, unsupported questions, restricted documents, and prompt-injection-style attempts to reveal restricted content. `AnswerQualityScorer` provides a model-judge extension contract, while the required gate remains keyless and deterministic.

## Production extension

A production deployment can replace the local pieces with:

- Next.js on Vercel Enterprise or AWS
- FastAPI/LangGraph on ECS/Fargate
- Aurora/RDS PostgreSQL with pgvector
- S3 for source documents
- SQS + workers for ingestion and offline evaluations
- ElastiCache/Redis for justified ephemeral state
- OIDC/SAML SSO
- tenant/user ACL filters enforced in database/vector queries
- tracing and production evaluation telemetry

Those components are architecture extensions. This repository does **not** claim that they are provisioned or live.
