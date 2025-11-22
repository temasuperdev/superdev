<!-- This file is generated/updated by an AI assistant. Please review before committing. -->
# copilot-instructions for superdev

Purpose: give precise, repo-specific guidance so an AI agent can be productive immediately.

**Repository State (current)**: The repo now contains a minimal FastAPI scaffold with async SQLite:
- `requirements.txt` — Python dependencies
- `app/` — application package (`database.py`, `models.py`, `schemas.py`, `crud.py`, `main.py`)
- `tests/test_basic.py` — pytest async test
- `dev.db` (created at runtime)

If you open the code, the key integration is FastAPI + `databases` (async) + SQLAlchemy Table metadata.

**When making changes or implementing features**:
- **Confirm design intent first:** Ask if the app should remain a single-process SQLite dev prototype vs. a production service (Postgres, migrations, connection pool).
- **Follow existing structure:**
	- DB connection and metadata live in `app/database.py` (use `database` and `metadata` there).
	- Table definitions live in `app/models.py` using SQLAlchemy `Table` objects.
	- Async DB access goes through small helpers in `app/crud.py` using `databases.Database` queries.
	- Request/response models live in `app/schemas.py` (Pydantic).
	- Routes and lifecycle are in `app/main.py` (startup connects DB + creates tables via `metadata.create_all(engine)`).

**Developer commands / workflows**
- Create virtualenv (optional):
	- `python -m venv .venv && source .venv/bin/activate`
- Install dependencies:
	- `python -m pip install -r requirements.txt`
- Run local server:
	- `uvicorn app.main:app --reload`
- Run tests (uses `pytest` + `pytest-asyncio`):
	- `pytest -q`

Notes about tests: the included test uses `httpx.AsyncClient` with `ASGITransport` to exercise the FastAPI app in-process. Tests create tables with `metadata.create_all(engine)` and remove `dev.db` after run.

**Project-specific conventions & gotchas**
- SQLite file: the scaffold uses `sqlite:///./dev.db`. Keep this localized for development — for CI or prod prefer a dedicated DB.
- Table creation: the app calls `metadata.create_all(engine)` on startup. For anything beyond prototypes, add migrations (Alembic) instead of relying on `create_all`.
- Async DB: use `databases.Database` for async queries (see `app/database.py`). Do not mix sync DB calls on code paths expected to be async.
- Pydantic v2 notes: this repo currently uses Pydantic v2 where `orm_mode` is deprecated (warning). When adding/adjusting models, prefer `model_dump()` over `.dict()` and migrate `orm_mode` → `from_attributes` if you adopt v2 idioms.
- FastAPI deprecation: `@app.on_event("startup")` is used for simplicity; consider `lifespan` for newer FastAPI versions.

**Integration points / extension notes**
- To add background workers or queues, create a separate package (e.g., `worker/`) and share DB models via the `app/models.py` module.
- To add migrations: add `alembic` and configure it to use the SQLAlchemy `metadata`.

**Files to inspect when changing behavior**
- `app/database.py` — DB URL, `database`, `metadata`, `engine`
- `app/models.py` — table schemas
- `app/crud.py` — async DB access patterns
- `app/schemas.py` — public API types (Pydantic)
- `app/main.py` — API endpoints and lifecycle
- `tests/test_basic.py` — example of testing approach (ASGI transport, pytest-asyncio)

**If blocked or unsure**
- Ask these concrete questions:
	- Should we keep SQLite for production or switch to Postgres/MySQL?
	- Do you prefer migrations (Alembic) or `create_all` for now?
	- Preferred test strategy: in-memory DB, ephemeral file DB, or testcontainers?

If you want, I can now:
- Add Alembic + migration example, or
- Replace startup events with an explicit `lifespan` context, or
- Expand the API (items, auth) and add CI workflow for tests.
