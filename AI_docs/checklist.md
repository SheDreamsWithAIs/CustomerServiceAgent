# Project Checklist: Customer Service Chatbot with Multi-Agent Routing

This checklist is a living guide for building your agentic customer service chatbot. We'll mark items as we complete them, and add details as the project grows.

---

## Foundation & Initial Setup
- [ ] Review project specs and grading rubric
- [ ] Set up project repository and folders
- [ ] Install required Python packages
- [ ] Prepare requirements.txt and environment variables
- [ ] Review sample code and lessons (LangChain quickstart, etc)

---

## Core System Design
- [ ] Draft system prompt for supervisor/routing agent
- [ ] Define agent responsibilities:
  - [ ] Billing agent
  - [ ] Technical support agent
  - [ ] Policy & compliance agent
  - [ ] Emotional support ("dad joke") agent
- [ ] Choose model(s) (OpenAI, AWS Bedrock where appropriate)
- [ ] Plan/diagram agent routing and tool calls

---

## Document Loading & RAG Pipeline
- [ ] Load documents using LangChain loader(s) (PDF, text, markdown, etc)
- [ ] Split documents into chunks (text splitters)
- [ ] Create vector embeddings for chunks (OpenAIEmbeddings or similar)
- [ ] Store/retrieve chunks with ChromaDB vector store (use explicit collection_name and absolute paths)
- [ ] Run similarity search queries (vectorstore only)
- [ ] Integrate LLM (true retrieval-augmented generation)
- [ ] Pass retrieved context to LLM and synthesize final answer
- [ ] Implement two-step RAG (retriever always runs before LLM) where required
- [ ] Implement agentic RAG (agent/model decides when to trigger retrieval) where required
- [ ] Document/debug best practices for vector DB paths and chunking for robust RAG

- Model Context (apply where relevant):
  - [ ] Use `dynamic_prompt` middleware to adapt system instructions by conversation state (tone, conciseness)
  - [ ] Use `wrap_model_call` to inject session/file context into model calls when needed
  - [ ] Implement dynamic model selection for cost/performance balance (middleware)
  - [ ] Use structured `response_format` (Pydantic/dataclass) for predictable outputs where helpful

> This pipeline enables question-answering or summarization based on custom documents, not just the language model’s original knowledge.

---

## Agent Patterns, Memory & Implementation

Below is a unified design + implementation plan for each agent.  This merges the conceptual patterns (RAG/CAG/hybrid) with concrete implementation tasks so the rubric alignment is clear and there are no conflicting lists.

- Routing Agent (CAG only)
  - Design: Handles session context, user intent, and message history. Routes incoming messages to subagents based on content and session state. Does not retrieve from a vector DB.
  - Implementation:
    - [ ] Define `RoutingContext` dataclass with fields: `user_id`, `thread_id`, `last_intent`, `last_agent`, `session_vars`.
    - [ ] Implement intent classification (keyword-based or lightweight model) to map queries to agents.
    - [ ] Ensure supervisor can call subagents as tools and pass runtime `context` and `config`.
    - [ ] Add unit tests for routing logic and ambiguous intent handling.

- Technical Support Agent (PURE RAG)
  - Design: Always perform retrieval from a support knowledge base (two-step RAG). Use KB content to build answers and troubleshooting steps.
  - Implementation:
    - [ ] Create a dedicated support KB and ingestion script (load, split, embed, persist in ChromaDB) with explicit `collection_name` and absolute paths.
    - [ ] Wrap retrieval as a `@tool` returning structured outputs (e.g., `summary`, `steps`, `source_page`).
    - [ ] Implement the agent so it MUST perform retrieval before answering (two-step RAG per rubric).
    - [ ] Add fallback messaging and escalation path for empty retrievals or complex/unknown issues.

- Billing Agent (HYBRID: RAG + CAG)
  - Design: Combine retrieval from billing docs (RAG) with injected user/account/session context (CAG) so responses are personalized and accurate.
  - Implementation:
    - [ ] Maintain `BillingContext` dataclass with `account_id`, `last_invoice_id`, `open_tickets` and other minimal user/account info.
    - [ ] Use retrieval for billing docs (policy, invoices, FAQ) and inject the user/account state into prompts.
    - [ ] Implement a secure mock tool to fetch user-specific records (in-memory or simple JSON) for demo purposes.
    - [ ] Test personalized billing queries and multi-turn continuity.

- Policy Agent (PURE CAG)
  - Design: Always uses injected policy/context (CAG). Answers should be derived from the authoritative policy snapshot supplied to the agent at runtime; no vector retrieval for core policy decisions.
  - Implementation:
    - [ ] Implement `PolicySnapshot` dataclass/config that can be injected as system prompt material for each policy query.
    - [ ] Ensure the agent refuses or flags requests outside policy and logs decisions for audit.
    - [ ] Add tests for edge cases (missing policy context, unauthenticated user, conflicting rules).

- Dad Joke Agent (CONTEXT-FILTERED RAG + CAG)
  - Design: Retrieve jokes from a small joke DB, filter by recent user conversation topics or puns (CAG), and prefer topical jokes; fallback to general jokes where necessary.
  - Implementation:
    - [ ] Build a dad-joke DB with metadata tags (`topic`, `pun_keywords`, `tone`).
    - [ ] Implement a retriever tool (`@tool`) that accepts `preferred_topics` and returns top jokes.
    - [ ] Capture recent user keywords/messages in a context dataclass and pass them as retrieval filters.
    - [ ] Add content filtering and safe-fallback behavior.

- Tool Context (apply across specialist agents):
  - [ ] Ensure tools read from `runtime.state`, `runtime.store`, and `runtime.config` with safe defaults
  - [ ] Use `Command(update={...})` for all tool writes that change state or store
  - [ ] Check permissions before performing sensitive tool actions (auth, premium tools)
  - [ ] Add unit tests for store/state read/write patterns and tool error handling

- Integration & Testing
  - [ ] Register all agents/tools with the supervisor orchestration layer (routing agent).
  - [ ] Validate context propagation, tool-call tracing, and hand-offs between agents (use simple mock sessions).
  - [ ] Add monitoring/logging hooks for debugging and grading (trace tool calls, retrieval scores, and policy decisions).
  - [ ] Test end-to-end flows including happy-path and adversarial scenarios so grading rubric criteria are demonstrable.
  - [ ] Add `handoff_to_supervisor` tool to each specialist agent (technical, billing, policy, dad joke)
    - Tool should set a runtime flag or return a Command so the supervisor knows to resume control
    - Ensure specialists never directly compose final user-facing messages when handing off
  - [ ] Supervisor composes unified, persona-aware user messages
    - Supervisor reads tool output and persona hints and returns a single message to the user
    - Specialist internal traces must be logged but not shown to the user
    - Add tests to verify handoff UX (user sees only a smooth persona-aware transition)

- Persona Hints & Supervisor Prompting
  - [ ] Define a `persona_hint` schema and allowed values (e.g., `"neutral"`, `"helpful"`, `"humorous"`, `"formal"`).
  - [ ] Specialists should include `persona_hint` and optional `persona_metadata` (e.g., `persona_tone`, `persona_length`, `persona_emphasis`) when returning tool results to the supervisor.
  - [ ] Supervisor must map `persona_hint` to system-prompt templates (persona templates) and apply those templates when composing the final user-facing message.
  - [ ] Ensure persona switching is surface-level (tone/wording) only; never expose internal agent names to users.
  - [ ] Log persona_hint usage for auditing and grading; add tests to validate persona application and smooth transitions.

> This unified section ensures each agent's pattern (PURE RAG, PURE CAG, HYBRID) is explicit and mapped to concrete implementation tasks that match the rubric. All items remain unchecked for manual tracking in your main project repository.

---

## Chat UI & Integration
- [ ] Choose front-end technology (Streamlit, Flask, React, etc)
- [ ] Build basic chat interface
- [ ] Connect frontend to agent backend (API, websocket, etc)

---

## Testing & Polish
- [ ] Test all agent routing scenarios
- [ ] Test UI/UX with sample user flows
- [ ] Refine/promote helpful, friendly/engaging responses
- [ ] Optimize for speed, cost, and reliability
- [ ] Prepare for hand-off/submission

---

## Documentation
- [ ] Write project README
- [ ] Document design decisions and how to run code
- [ ] Ensure rubric requirements are satisfied

---

## (Add new tasks as needed!)
