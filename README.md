# Multiagent Fullstack Project Orchestrator

A web application where you describe a software project in plain English, and **7 specialized AI agents** (powered by Anthropic `claude-sonnet-4-6`) coordinate to build it — streaming real-time progress to your browser.

## How It Works

```
You describe a project
        ↓
Planner Agent → Architecture Document
Researcher Agent → Research Brief (parallel)
        ↓
You review & approve the architecture
        ↓
4 agents build in parallel:
  Frontend Agent  |  Backend Agent  |  Database Agent  |  DevOps Agent
        ↓
Files written to disk — browse them in the UI
        ↓
Request changes with natural language → Update Agent
```

## Prerequisites

- Python 3.12+
- Node.js 22+
- An [Anthropic API key](https://console.anthropic.com)
- Docker & Docker Compose (optional — for full stack)

## Quick Start (Local Dev — no Docker)

### 1. Setup

```bash
git clone <your-repo-url>
cd multiagent-orchestrator
cp .env.example .env
# Edit .env — set ANTHROPIC_API_KEY
```

### 2. Generate JWT keys

```bash
cd backend
python -m scripts.generate_keys
```

### 3. Start the backend

```bash
cd backend
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

Backend runs at http://localhost:8000

### 4. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

---

## Docker Quick Start (Full Stack)

```bash
cp .env.example .env
# Edit .env: set ANTHROPIC_API_KEY and POSTGRES_PASSWORD

docker compose up --build
```

Open http://localhost:80

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | ✅ | — | Your Anthropic API key |
| `DATABASE_URL` | ✅ | SQLite dev | PostgreSQL or SQLite connection URL |
| `OUTPUT_DIR` | | `./output` | Where generated project files are written |
| `JWT_PRIVATE_KEY_PATH` | | `./keys/private.pem` | RS256 private key (auto-generated if missing) |
| `JWT_PUBLIC_KEY_PATH` | | `./keys/public.pem` | RS256 public key |
| `ALLOWED_ORIGINS` | | `localhost:5173` | CORS allowed origins |
| `MAX_SESSIONS_PER_USER` | | `2` | Max concurrent build sessions per user |
| `API_SEMAPHORE_LIMIT` | | `3` | Max concurrent Anthropic API calls |
| `POSTGRES_PASSWORD` | Docker | — | PostgreSQL password |

---

## Using the App

1. **Register** an account at `/register`
2. **Create a project** — click "New Project" and describe what you want built
3. **Wait** for Planner and Researcher agents (~1-2 minutes)
4. **Review** the Architecture Document in the browser
5. **Approve** — click "Approve & Build" to start the parallel build
6. **Watch** 4 agents build your project in real time
7. **Browse** generated files in the file explorer
8. **Request changes** with natural language

---

## Agent Roles

| Agent | Role |
|---|---|
| **Planner** | Produces Architecture Document (tech stack, directory structure, API contract, component tree) |
| **Researcher** | Produces Research Brief (package versions, security checklist, patterns) |
| **Frontend** | Builds all UI components, pages, hooks, state management |
| **Backend** | Builds all API routes, business logic, auth, middleware |
| **Database** | Designs schema, writes migrations, seeds data |
| **DevOps** | Writes Dockerfiles, docker-compose, GitHub Actions CI/CD, README |
| **Update** | Handles change requests — analyzes impact, produces Change Plans |

---

## Development

### Running tests

```bash
# Backend
cd backend && pytest -v

# Frontend
cd frontend && npm test
```

### Code style

```bash
# Backend
cd backend && ruff check app/

# Frontend
cd frontend && npm run lint && npm run typecheck
```

### Pre-commit hooks

```bash
pip install pre-commit
pre-commit install
```

---

## Project Structure

```
multiagent-orchestrator/
├── backend/
│   ├── app/
│   │   ├── agents/          7 AI agent classes
│   │   ├── orchestrator/    Phase state machine
│   │   ├── routers/         FastAPI route handlers
│   │   ├── models/          SQLAlchemy ORM models
│   │   ├── schemas/         Pydantic request/response schemas
│   │   ├── bus/             asyncio message bus
│   │   └── services/        Anthropic client, file writer
│   ├── alembic/             Database migrations
│   └── tests/
├── frontend/
│   └── src/
│       ├── components/      React components
│       ├── hooks/           Custom React hooks
│       ├── store/           Zustand state slices
│       ├── api/             API client functions
│       └── pages/           Route-level pages
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Known Limitations

- **SQLite** is used by default (dev only). Switch to PostgreSQL for production multi-worker deployments.
- **Large projects** (~50k+ token output) may approach Anthropic rate limits; the system retries with exponential backoff.
- **Output files** are written to local disk — plan accordingly for containerized/cloud deployments (mount a persistent volume).
- **Single-server** deployment only in v1 — the in-process message bus doesn't support horizontal scaling. Use Redis for multi-instance deployments.

---

## License

MIT
