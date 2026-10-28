# CI/CD Task Manager workshop
Stack: React/Vite, FastAPI, MySQL (Aiven); Render static site + web service. GitHub Actions gates deployment via CI workflow completion on main. Configure BOTH Render services with Auto-Deploy **Off**, and add deploy hooks to GitHub Actions secrets. The manual workflow_dispatch path demonstrates continuous delivery; workflow_run on main demonstrates continuous deployment. Deploy hooks initiate builds asynchronously; green deploy workflow means hooks accepted, not that deployed app is healthy. Verify Render deploy logs and /health afterward. For stronger guarantees add health polling and immutable release identifiers.

## Local quickstart
Backend: `cd backend && python3.11 -m venv .venv && source .venv/bin/activate && pip install -r requirements-dev.txt && ruff check . && bandit -q -r app && pytest -q && uvicorn app.main:app --reload`
Frontend: `cd frontend && npm install && npm run lint && npm test && npm run build && npm run dev`
On Windows use `.venv\Scripts\activate` instead of `source ...`.

## Critical constraints
CI tests use SQLite, production uses Aiven MySQL. MySQL-specific integration behavior is NOT exercised by SQLite tests. Do not commit credentials. GitHub branch protection may be unavailable on private repositories under free plans: use a PUBLIC educational repo with required status checks where available, or instructor-controlled merge policy. Each pair should fork/template into its own repo so each can configure their own deploy hooks.
