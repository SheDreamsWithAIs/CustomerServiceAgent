<!-- cab9b525-30ae-4ad9-9e78-83a513991e00 91d786c0-3312-467d-8c67-db369e31634d -->
# Agentic Customer Service Chatbot — Best-Practice Phased Plan

Aligned with `AI_docs/checklist.md`, rubric/specs, and your choices: Vibe Coding Strategy; wire OpenAI and Bedrock from the start but gate usage until later phases. We will verify every backend step in Swagger before integrating the frontend.

## Phase 0 — Project Scaffolding (Best Practices, Swagger-first)

- Backend structure (Python/FastAPI):
- `backend/`
  - `app/main.py` (create app, mount routers, CORS)
  - `app/api/v1/` (versioned API)
  - `routers/health.py` (GET `/api/v1/health`)
  - `routers/providers.py` (GET `/api/v1/providers` non-secret diag)
  - `routers/chat.py` (POST `/api/v1/chat`)
  - `app/core/config.py` (Pydantic `BaseSettings` for env)
  - `app/core/providers.py` (model/provider registry & factory)
  - `app/schemas/` (Pydantic request/response models)
  - `app/retrieval/` (Chroma client, retriever helpers)
  - `app/ingest/` (ingestion scripts)
  - `app/agents/` (agents definitions)
  - `app/tools/` (LangChain tools)
  - `tests/` (pytest)
- Use `requirements.txt` (FastAPI, Uvicorn, Pydantic, python-dotenv, langchain>=1.0, langgraph>=1.0, chromadb, langchain-openai, boto3/bedrock libs)
- `.env.example` (placeholders only; never print secrets)
- OpenAPI at `/docs`, versioned API base `/api/v1`
- Verification: run server; Swagger lists `/api/v1/health` → 200 OK

## Phase 0F — Frontend Audit & Baseline Verification (use existing code)

- Confirm current stack (already present):
- Next.js 16, App Router under `frontend/src/app`
- React 19, Tailwind CSS v4 (zero-config via `@tailwindcss/postcss`), `globals.css`
- Routes detected: `/`, `/chat`, `/kb`, `/cart`
- Verification steps against existing UI:
- Run `npm run dev` in `frontend/`; open `/`, `/chat`, `/kb`, `/cart` to confirm pages render
- Confirm Tailwind styles applied (check typography, spacing, colors)
- Ensure existing components render on `/chat` (`AgentBadge`, `ChatHeader`, `ChatSidebar`, `MessageBubble`)
- Note: no `tailwind.config.*` is expected with v4; keep zero-config unless needed

## Phase 1 — Provider Wiring (OpenAI + Bedrock, gated usage)

- `app/core/providers.py`: initialize providers via env (enabled flags, region, model names)
- Model registry strings (e.g., `openai:gpt-4o-mini`, `bedrock:anthropic:haiku`)
- `/api/v1/providers` returns enabled provider NAMES only (no secrets)
- Verification: Swagger GET providers shows expected names

## Phase 2 — API Contracts (Mocked agent)

- `app/schemas/chat.py`: `ChatRequest{message,user_id,thread_id}`, `ChatResponse{message,route?}`
- Implement `/api/v1/chat` returning a mocked echo response with `route="echo"`
- Clear tags/descriptions for Swagger
- Verification: Swagger POST `/api/v1/chat` returns structured mocked response

## Phase 3 — RAG Infra: Ingestion + Vector Store

- `app/ingest/ingest_data.py`: load sample docs (PDF/MD/TXT), split, embed, persist to Chroma (`persist_directory`, `collection_name`)
- `app/retrieval/retriever.py`: similarity and MMR helpers
- CLI verification: run ingestion; quick internal check returns top-3 docs for test query

## Phase 4 — Technical Support Agent (Pure RAG, two-step)

- Mandatory LangChain v1.0 docs check before coding
- `app/tools/search_documents.py` (Chroma search tool)
- `app/agents/technical.py`: create agent via `create_agent()` enforcing retrieve-then-answer
- `/api/v1/chat?mode=tech_support` routes to tech agent
- Verification: Swagger POST returns answer citing retrieved context

## Phase 5 — Policy Agent (Pure CAG)

- `PolicySnapshot` loader (inject static policy context; no vector search for policy decisions)
- `/api/v1/chat?mode=policy` routes to policy agent
- Verification: Answers grounded in policy; denies out-of-policy asks

## Phase 6 — Billing Agent (Hybrid: RAG + CAG)

- `BillingContext` + mock account lookup tool (safe, demo-only)
- RAG over billing docs + inject account/session context
- `/api/v1/chat?mode=billing`
- Verification: Personalized answers; graceful fallback when account missing

## Phase 7 — Supervisor/Routing (Tool-calling pattern)

- Supervisor via `create_agent()`; sub-agents wrapped as tools; light intent classification; persona hints
- Make `/api/v1/chat` default to supervisor; `mode` optional override
- Verification: Swagger routes prompts to correct agent; logs identify agent

## Phase 8 — Middleware: Context Engineering & Memory

- Summarization middleware to manage long chats
- Dynamic prompt for tone/conciseness; optional model selection middleware (use Bedrock for routing, OpenAI for answers)
- Verification: Long conversations remain responsive; provider choice visible in non-secret diagnostics

## Phase 9 — Frontend Integration Using Existing App Router

- Use current structure in `frontend/src/app` and components in `frontend/src/components`
- API config: `NEXT_PUBLIC_API_BASE_URL` env; fallback `http://localhost:8000`
- Add a lightweight client helper in `frontend/src/lib/api.js` (fetch wrapper)
- `/chat` page: wire send → POST backend `/api/v1/chat` (no streaming yet)
- Optional Next rewrite in `next.config.mjs` to proxy `/api/*` to backend to avoid CORS
- Verification against existing UI:
- From `/chat`, send a message and render response from mocked backend
- Confirm no CORS issues (either via CORS or Next.js rewrites)
- Verify pages still load (`/`, `/kb`, `/cart`) and styles remain intact

## Phase 10 — Streaming & UX Polish

- SSE/streaming from backend; token-by-token render in UI
- Persona-aware responses surfaced; light UI polish
- Verification: Streaming visible; rubric streaming criteria met

## Phase 11 — Tests, Observability, Docs

- Pytest unit tests: retriever, routing, tools, fallbacks
- Basic logging/trace hooks; README and runbook
- Verification: Tests green; rubric items demonstrable

## Notes & Constraints

- Always check LangChain/LangGraph v1.0 docs before agent changes
- Never expose secrets; provider usage gated
- Keep steps small; verify in Swagger before UI integration

### Optional DX Enhancements (can slot into Phase 0 or later)

- Add `ruff`/`black`, pre-commit, and `mypy` for type checking
- Simple CI (lint + tests)

### To-dos

- [ ] Create backend skeleton, /health, requirements, CORS; verify in Swagger
- [ ] Wire OpenAI and Bedrock configs and registry; add /providers; verify
- [ ] Define ChatRequest/ChatResponse and mocked /chat endpoint; verify in Swagger
- [ ] Implement ingestion to Chroma and basic retriever; verify locally
- [ ] Build Technical Support agent (Pure RAG) and mode switch; verify in Swagger
- [ ] Build Policy agent (Pure CAG) and mode switch; verify in Swagger
- [ ] Build Billing agent (Hybrid RAG+CAG) with mock account; verify
- [ ] Create supervisor with sub-agents as tools and routing; verify
- [ ] Add summarization, dynamic prompts, model selection middleware; verify
- [ ] Create Next.js chat UI and connect to backend; verify basic flows
- [ ] Implement streaming responses and UI polish; verify rubric criteria
- [ ] Add tests, logging, README, and final verification against rubric

