# OfficeLifeline – Multi‑Agent Customer Service App

Full‑stack demo with a FastAPI backend (LangChain v1.0, LangGraph) and a Next.js 16 frontend.

## Requirements
- Python 3.11+
- Node 20+
- An OpenAI API key in your environment (`OPENAI_API_KEY`)

## Backend (FastAPI)

### Install
```powershell
cd backend
python -m venv ..\venv
..\venv\Scripts\activate
pip install -r requirements.txt
```

### Run
```powershell
# From backend/
python -m uvicorn app.main:app --reload --port 8000
```
- Swagger: http://localhost:8000/docs
- Health: `GET /api/v1/health`
- Providers: `GET /api/v1/providers`
- Chat (JSON): `POST /api/v1/chat`
- Chat (SSE stream): `POST /api/v1/chat/stream`

Example request body:
```json
{
  "message": "Where can I find data privacy settings?",
  "user_id": "user_123",
  "thread_id": "t1"
}
```

Notes:
- `thread_id` starts a new conversation when you provide a new value.
- Modes (optional): `?mode=technical`, `?mode=policy`, `?mode=billing`.
- Default routing uses a supervisor agent; billing is guarded to use account info when `user_id` is present.

### Knowledge Base (Chroma)
Reindex the demo docs:
```powershell
# From repo root
powershell -NoProfile -ExecutionPolicy Bypass -File .\AI_docs\scripts\reindex.ps1
```
- Sources are under `backend/documents_for_agents/`
- Vector store persists in `backend/.chroma`

## Frontend (Next.js 16)

### Install & Run
```powershell
cd frontend
npm install
# set backend API base if needed
$env:NEXT_PUBLIC_API_BASE_URL="http://localhost:8000"
npm run dev
```
Open http://localhost:3000/chat

### Chat UI
- Streams text from `/api/v1/chat/stream`, then fetches JSON for structured fields (billing summary)
- “New Chat” starts a new thread without a page refresh

## Project Structure (selected)
```
backend/
  app/
    api/v1/routers/ (health, providers, chat)
    agents/ (technical, policy, billing, supervisor)
    tools/ (search_documents, billing_accounts)
    retrieval/ (Chroma retriever)
    ingest/ (ingest_data.py)
    middleware/ (summarization + dynamic prompt)
frontend/
  src/app/chat/page.js (UI wired to backend)
  src/lib/api.js (API client + SSE)
```

## Notes
- LangChain v1.0+ patterns (no legacy LCEL). Agents via `create_agent()`; memory via `InMemorySaver`.
- Streaming is SSE; UI renders progressively.
- Billing responses include a short structured summary.

## Troubleshooting
- “Could not connect to tenant default_tenant”: ensure we’re using `langchain_chroma` (already configured)
- Ingestion duplicates: current script does not dedupe; reindex script wipes and rebuilds
- PowerShell execution policy errors: run the script with `-ExecutionPolicy Bypass`

## License
Educational project for coursework/demo purposes.
