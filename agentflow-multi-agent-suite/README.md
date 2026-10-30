# AgentFlow Multi-Agent Suite

Autonomous, multi-agent AI career and form-filling platform. Aria (Chief of Staff) oversees 6 specialized agents with a live browser view inside the chat.

## Stack
- Backend: FastAPI (Python), Playwright, browser-use, OpenRouter
- Frontend: Vite + React + TypeScript + Tailwind CSS
- DB: SQLModel (SQLite dev / PostgreSQL prod)
- Realtime: WebSocket

## Quick Start (Dev)

### Backend
```bash
cd backend
cp .env.example .env
pip install -e .
playwright install chromium
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Features
- 7 agents: Aria (COS) + Scout, Profiler, Tailor, Navigator, Verifier, Executor
- Live browser rectangle in chat with frame streaming
- Auto-detect login -> yield to user, auto-takeover after login
- CAPTCHA/bot challenge detection -> yield to user
- Take control anytime mid-swarm, hand back to Aria
- Per-agent OpenRouter routing with strong free model fallbacks
- Renamable agents with unique colorful mascots
- Grok/Hark Pro inspired premium UI

## Deploy
Use provided Dockerfiles. Set env vars for Postgres + OpenRouter.
