# Global FastAPI Backend Template (WIP)

Modern, extensible backend template for Python developers built around ****FastAPI****, **async SQLAlchemy**, ****Pydantic****, and clean architecture patterns. This template is actively evolving and will integrate the most widely used tools and practices in modern backend development.

Status: Work In Progress (**WIP**). Planned integrations include **Docker**, **Docker Compose**, authentication (**JWT**/**OAuth2**), task queues, observability, **CI/CD**, and more.

This folder is part of a multi-project monorepo used to solve tasks in the `Quick-Start-in-FastAPI-Python` course. The end goal is to master a modern Python backend stack using best practices.

---

## Goals

- Provide a production-leaning, educational template with clear separation of concerns (**API**, **services**, **repositories**, **exceptions**).
- Showcase async-first design (****FastAPI**** + **async SQLAlchemy**).
- Standardize error handling and ****i18n****.
- Be easy to extend with new *endpoints*, *services*, *repositories*, and *infrastructure*.
- Serve as a global reusable template across sub-projects in the parent repository.

---

## Monorepo Context

This template lives under the monorepo root:

- Monorepo root: `Quick-Start-in-FastAPI-Python/`
- This template: `Quick-Start-in-FastAPI-Python/global_template/`

You can run, test, and migrate from either:

- The repo root (preferred): use fully qualified module paths (e.g., global_template.app.main:app)
- The global_template folder: use relative paths (e.g., app/main.py)

---

## Key Features (current)

- **FastAPI** application with modular routers (`todos`, `users`, `tags`, `user profiles`).
- **Async SQLAlchemy** setup (*engine*, *session*, *declarative base*).
- Repository and **Unit of Work** patterns.
- **Pydantic** v2 schemas for input/output validation and **OpenAPI** docs.
- Centralized exception hierarchy and consistent error responses.
- Internationalization (**i18n**) via **fastapi-babel** + middleware (en, ru catalogs scaffolded).
- **Alembic** migrations scaffold (alembic/ + alembic.ini present; versions directory ready).
- Basic test setup with **pytest** and **FastAPI** TestClient.

Planned (see Roadmap):

- **Docker** + **Docker Compose**
- Authentication/Authorization (**JWT**/**OAuth2**, **RBAC**)
- Deeper **Alembic** integration and generated migrations
- Async task processing (e.g., **Celery**/**RQ**) and caching (**Redis**)
- Observability (structured logging, Sentry, metrics)
- Linting/formatting/type checking (ruff/black/isort/mypy, pre-commit)
- **CI/CD** (GitHub Actions)
- **API** versioning, rate limiting, CORS hardening

---

## Repository Structure (focused on global_template)

High-level overview (not exhaustive):

```text
.
├── alembic
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
├── alembic.ini
├── app
│   ├── api
│   │   ├── endpoints
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   ├── tag.py
│   │   │   ├── todo.py
│   │   │   ├── userprofile.py
│   │   │   └── user.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   └── schemas
│   │       ├── __init__.py
│   │       ├── __pycache__
│   │       ├── tag.py
│   │       ├── todo.py
│   │       ├── userprofile.py
│   │       └── user.py
│   ├── core
│   │   ├── config.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   ├── db
│   │   ├── database.py
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── __pycache__
│   ├── exceptions
│   │   ├── core.py
│   │   ├── db_exceptions.py
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── tag_exceptions.py
│   │   ├── todo_exceptions.py
│   │   ├── user_exceptions.py
│   │   └── userprofile_exceptions.py
│   ├── i18n
│   │   ├── en
│   │   │   └── LC_MESSAGES
│   │   │       └── messages.po
│   │   ├── README.md
│   │   └── ru
│   │       └── LC_MESSAGES
│   │           └── messages.po
│   ├── __init__.py
│   ├── main.py
│   ├── __pycache__
│   ├── repositories
│   │   ├── base_repository.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── tag_repository.py
│   │   ├── todo_repository.py
│   │   ├── userprofile_repository.py
│   │   └── user_repository.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── tag_service.py
│   │   ├── todo_service.py
│   │   ├── userprofile_service.py
│   │   └── user_service.py
│   └── utils
│       ├── __init__.py
│       ├── __pycache__
│       └── unitofwork.py
├── __init__.py
├── __pycache__
├── .env
├── .env.example
├── README.md
└── tests
    ├── conftest.py
    ├── __init__.py
    ├── __pycache__
    └── test_todo.py
```

> Note: Some modules (e.g., user/tag schema, unit of work implementation) are referenced and expected to be present in the wider project.

---

## Tech Stack

- Language: **Python 3.12+** (recommended)
- Web framework: **FastAPI**
- Validation/serialization: **Pydantic** (v2)
- Database/ORM: **SQLAlchemy** (async), asyncpg (**PostgreSQL**)
- Settings: **pydantic-settings**
- **i18n**: **fastapi-babel**
- Testing: **pytest**, **FastAPI TestClient**
- ASGI server: **Uvicorn** (dev)

---

## Configuration

Environment variables (via `.env` or system envs) loaded by `pydantic-settings`:

- DB_HOST: database host
- DB_PORT: database port (e.g., 5432)
- DB_USER: database username
- DB_PASS: database password
- DB_NAME: database name
- JWT_SECRET_KEY: secret for token signing (placeholder for future auth)
- JWT_ALGORITHM: default HS256
- ACCESS_TOKEN_EXPIRE_MINUTES: default 1440 (24h)

Async DB URL is constructed as:
`postgresql+asyncpg://DB_USER:DB_PASS@DB_HOST:DB_PORT/DB_NAME`

The `.env` path is configured in `app/core/config.py` (relative to that file).

---

## Migrations (Alembic)

**Alembic** is scaffolded under `global_template/alembic` with configuration in `global_template/alembic.ini`.

Typical workflow (from repo root):

- Create a revision (autogenerate):
  - `alembic -c global_template/alembic.ini revision --autogenerate -m "initial"`
- Apply migrations:
  - `alembic -c global_template/alembic.ini upgrade head`
- Downgrade:
  - `alembic -c global_template/alembic.ini downgrade -1`

> Notes:
>
> - Ensure your DB env vars are set so **SQLAlchemy** connects correctly.
> - As the template evolves, model metadata and **env.py** may be adjusted.

---

## Architecture Overview

- API Layer (**FastAPI** routers): Defines endpoints, request/response models.
- Service Layer (business logic): Coordinates use cases, transactions, and error handling.
- Data Layer (repositories + unit of work): Encapsulates persistence operations and transaction boundaries.
- Exceptions: Centralized hierarchy with consistent **JSON** error responses.
- **i18n**: Translations resolved with message keys and parameters.

Flow (example for ToDo):
`HTTP request` -> `Router` (todo.py) -> `ToDoService` (business rules) -> `UnitOfWork` -> `Repository` -> `DB`

Errors raised as **AppBaseException** (or subclasses) are localized and returned as structured **JSON**.

---

## Internationalization (**i18n**)

- **fastapi-babel** is configured in `main.py` with **BabelMiddleware**.
- Translations directory: `global_template/app/i18n`
- Exceptions include message_key and message_params. The handler:
  - Resolves the message via _(message_key).format(**params)
  - Returns structured **ErrorResponseModel JSON**

Example keys:

- errors.todo.not_found
- errors.db.connection_error

Add translations in your **i18n** catalogs and keep keys consistent across exceptions.

---

## Error Handling

Core handler: `app/exceptions/core.py`

- Base class: `AppBaseException(status_code, error_code, message_key, message_params)`
- Specialized DB errors: `DBException` and subclasses (`DBConnectionError`, `DBRecordNotFound`, etc.)
- ToDo-specific errors: `ToDoException` and subclasses (`ToDoNotFoundError`, `ToDoIntegrityError`, etc.)
- **JSON** error format (**ErrorResponseModel**):
  - status_code: int
  - message: localized string
  - error_code: string code (for programmatic handling)

Response includes X-ErrorHandleTime header for debugging.

---

## Database Layer

- Async engine and session factory: `app/db/database.py`
- Declarative base with common fields (id, created_at, updated_at) and automatic pluralized `__tablename__`.
- Models: `User`, `UserProfile` (1-1), `ToDo` (belongs to User), `Tag` (M2M with ToDo via association table).

Relationships:

- `User` 1—N `ToDo`
- `User` 1—1 `UserProfile`
- `ToDo` N—M `Tag`

---

## API Quick Tour (ToDos)

Router prefix: `/todos`

- `GET /todos`
  - Returns list[ToDoFromDB]
- `GET /todos/{todo_id}`
  - Returns ToDoFromDB, 404 if not found
- `POST /todos`
  - Body: ToDoCreate
  - Returns created ToDoFromDB, 201
- `PUT /todos/{todo_id}`
  - Body: ToDoUpdate (partial)
  - Returns updated ToDoFromDB
- `DELETE /todos/{todo_id}`
  - Returns 204 No Content

Example:

```json
Create ToDo

curl -X POST http://127.0.0.1:8000/todos
  -H "Content-Type: application/json"
  -d '{
        "title": "Learn FastAPI",
        "description": "Build a modern API",
        "completed": false,
        "user_id": 1,
        "tag_ids": [1,2]
      }'
```

```json
Error format

{
  "status_code": 404,
  "message": "Todo 3 was not found",
  "error_code": "todo_not_found"
}
```

> Note: Actual localized message depends on active locale and translations.

---

## Testing

- Pytest-based test suite.
- `tests/conftest.py` provides a `client` fixture using **FastAPI** `TestClient`.
- Run tests:
  - From repo/project root: pytest -q

For async DB operations, prefer service/repository integration tests with isolated DB (e.g., ephemeral schema, transaction rollbacks). Dedicated fixtures and Dockerized test DB will be added in the roadmap.

---

## Extending the Template

- Add a new feature/domain:
  1) Create **Pydantic** schemas in `app/api/schemas/<domain>.py`
  2) Add **ORM** models in `app/db/models.py` (or split by module as project grows)
  3) Create repository subclass in `app/repositories/<domain>_repository.py`
  4) Implement service in `app/services/<domain>_service.py` using UnitOfWork
  5) Add router in `app/api/endpoints/<domain>.py`
  6) Register router in `app/main.py`
  7) Write tests in `tests/`

Also:

- Add translations for new error messages and UI strings to `app/**i18n**`.
- Keep exception handling consistent by deriving from `AppBaseException` or a domain-specific parent exception.

---

## Roadmap

Infrastructure:

- [ ] Dockerfile(s) for dev and production
- [ ] Docker Compose (app + Postgres + Redis)
- [ ] Environment parity across dev/stage/prod

Auth & Security:

- [ ] OAuth2/JWT auth flows
- [ ] Password hashing and user management
- [ ] Role-based access control (RBAC)
- [ ] CORS, rate limiting, security headers

Data:

- [ ] Alembic migrations
- [ ] Seed scripts/fixtures
- [ ] Transactional test DB setup

Async & Caching:

- [ ] Task queue (Celery or RQ) with Redis
- [ ] Caching layer (Redis)

Quality & Tooling:

- [ ] pre-commit hooks (ruff/black/isort/mypy)
- [ ] Lint/type-check in CI (GitHub Actions)
- [ ] Unit/integration test matrix in CI

Observability:

- [ ] Structured logging (loguru/std logging config)
- [ ] Error tracking (Sentry)
- [ ] Metrics (Prometheus) and dashboards (Grafana)
- [ ] Health/readiness probes

API:

- [ ] API versioning strategy
- [ ] Pagination, filtering conventions
- [ ] Consistent response envelopes (if desired)

Docs:

- [ ] Developer Guide
- [ ] Operations Guide
- [ ] API Reference enhancements

---

## Using This Template Across the Monorepo

- Treat `global_template` as a shared foundation for sub-projects built during the course.
- When starting a new sub-project:
  - Copy or scaffold from `global_template`
  - Adjust settings, models, and routers to the project’s domain
  - Keep the folder layout and patterns for consistency across the repository

As the template evolves (new infra, tooling, policies), rebase or selectively merge updates into sub-projects to keep them aligned with modern practices.

---

## Contributing

Contributions are welcome. For consistency:

- Follow the structure/patterns used in services, repositories, and exceptions.
- Write tests for new features and maintain code coverage.
- Keep documentation in English and update README/roadmap as needed.
- For larger changes, propose an approach first (issues/discussions).

---

## License

Specify your license of choice for the repository (e.g., MIT, Apache-2.0). If none specified, default to your organization’s standard.

---

## Acknowledgments

- **FastAPI** and the async Python ecosystem.
- SQLAlchemy team for async ORM support.
- The `“Quick-Start-in-FastAPI-Python”` course context guiding this template’s scope and goals.
