# Enterprise AI Assistant — Next.js + Python + LangGraph

A compact, production-oriented reference implementation for a streamed, retrieval-grounded enterprise AI assistant. The repository is intentionally small enough to defend end to end in a technical interview while still demonstrating senior full-stack AI engineering patterns.

## What is implemented

- **Next.js 16 App Router** with a server-first page shell
- **React/TypeScript client boundary** limited to the interactive chat subtree
- **Next.js Route Handler BFF** that forwards an upstream response stream without buffering the complete answer
- **Python/FastAPI** API with typed request/event contracts
- **LangGraph orchestration** for retrieval → grounded answer composition
- **Authorization-aware retrieval** that applies tenant/user scope before ranking
- **RAG-style citations** with browser-safe metadata only
- **NDJSON HTTP streaming** with token, citation, error, and done events
- **Deterministic golden-dataset evals** covering regressions, refusals, ACL boundaries, and prompt injection
- **Model-judge extension protocol** without making paid APIs a default dependency
- **Docker Compose and GitHub Actions definitions** for local/CI execution

The default assistant uses a deterministic seeded knowledge base and requires no LLM API key.

## Repository layout

```text
apps/
  api/   FastAPI, LangGraph, retrieval, streaming, tests
  web/   Next.js App Router, BFF, chat UI, stream parser

evals/  golden dataset, deterministic scorers, eval runner

docs/   architecture and implementation/design records
```

## Request flow

```text
Browser
  ↓ POST /api/chat
Next.js Route Handler (BFF)
  ↓ POST /v1/chat/stream
FastAPI
  ↓
LangGraph
  ↓
Authorization-aware retrieval
  ↓
Grounded answer + safe citations
  ↓ NDJSON stream
Browser incremental render
```

See [`docs/architecture.md`](docs/architecture.md) for trust boundaries and the production scaling story.

## Run locally

### Option A — Docker Compose

```bash
docker compose up --build
```

Then open `http://localhost:3000`.

### Option B — services separately

API on macOS/Linux:

```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

API on PowerShell:

```powershell
cd apps/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Web on macOS/Linux:

```bash
cd apps/web
npm install
AI_API_BASE_URL=http://127.0.0.1:8000 npm run dev
```

Web on PowerShell:

```powershell
cd apps/web
npm install
$env:AI_API_BASE_URL = "http://127.0.0.1:8000"
npm run dev
```

Open `http://localhost:3000`.

## Try it

Good seeded questions include:

- `How should production agent changes be evaluated?`
- `When should authorization be applied in RAG retrieval?`
- `Is streaming always the same protocol for every realtime AI experience?`

The knowledge base intentionally contains a restricted document. The regular demo identity cannot retrieve it.

## Backend tests

```bash
cd apps/api
python -m pytest -q
python -m ruff check app tests
```

## Deterministic evaluations

From the repository root:

```bash
PYTHONPATH=apps/api:evals python evals/run_evals.py
PYTHONPATH=apps/api:evals python -m pytest evals/test_scorers.py -q
```

The runner exits non-zero if a deterministic regression is detected.

The dataset checks:

- expected citations
- required grounded answer content
- unsupported-question behavior
- tenant/user retrieval boundaries
- restricted-document leakage
- prompt-injection-style attempts

## Frontend checks

```bash
cd apps/web
npm test
npm run typecheck
npm run lint
npm run build
```

## Why two services?

Next.js owns rendering, browser interaction, and the BFF boundary. FastAPI/LangGraph owns AI orchestration, retrieval, and model-runtime concerns. That separation allows independent scaling, dependency management, testing, and observability instead of forcing Python AI workloads into the web runtime.

## Why NDJSON streaming?

A normal AI text-generation interaction is predominantly server-to-client after the request begins. A streamed HTTP response keeps the protocol inspectable and easy to test without requiring a persistent bidirectional socket. The browser parser deliberately handles JSON records that arrive split across arbitrary network chunks.

For realtime duplex voice or persistent bidirectional collaboration, WebSockets or a dedicated realtime transport would be a better fit.

## Evaluation philosophy

A prompt or orchestration change should not ship because five manual spot checks look better. The minimum safe path represented here is:

```text
baseline
  -> candidate change
  -> representative golden dataset
  -> deterministic regression checks
  -> optional model-based quality scoring
  -> canary / feature flag
  -> production metrics
```

Deterministic checks are preferred for facts such as citation identity, ACL behavior, event schema, and refusal expectations. Model-based scoring belongs on top for qualities such as relevance, completeness, faithfulness, and groundedness.

## Production path — documented, not provisioned

A production version could run Next.js on Vercel Enterprise or AWS, FastAPI/LangGraph on ECS/Fargate, source documents in S3, PostgreSQL/pgvector on RDS/Aurora, async ingestion/evals through SQS workers, and OIDC/SAML for enterprise identity.

Those services are **not** claimed as implemented by this MVP. The current working retrieval implementation is in-memory; `PgVectorRetriever` is an explicit adapter boundary for the production replacement.

## Portfolio competencies demonstrated

This repository provides inspectable evidence for:

- Python backend engineering and async API design
- Next.js App Router concepts
- React/TypeScript integration
- agent orchestration
- RAG and vector-search-oriented interfaces
- HTTP response streaming
- evaluation-driven AI development
- secure retrieval boundaries
- production architecture trade-offs
- end-to-end ownership across frontend, backend, tests, evals, CI, and documentation
