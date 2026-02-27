# Report System API

REST API for managing player reports, built with FastAPI and PostgreSQL.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## Overview

A clean, layered REST API for managing player reports. Designed to be consumed by Minecraft plugins, Discord bots, or any web frontend. Supports filtering, pagination, role-based access, and structured logging.

## Stack

- Python 3.11+
- FastAPI
- SQLAlchemy 2 (async)
- PostgreSQL + asyncpg
- Alembic
- JWT (python-jose)
- bcrypt (passlib)
- slowapi (rate limiting)
- structlog
- pytest + pytest-asyncio

## Architecture

```
app/
├── core/           config, database, security, logging
├── models/         SQLAlchemy ORM models
├── schemas/        Pydantic request/response schemas
├── repositories/   Database access layer
├── services/       Business logic
└── routes/         FastAPI routers
```

## Running locally

### With Docker

```bash
cp .env.example .env
docker-compose up --build
```

### Without Docker

```bash
cp .env.example .env
# Edit .env with your database credentials

pip install -r requirements.txt

alembic upgrade head

uvicorn app.main:app --reload
```

## API

Interactive documentation available at `http://localhost:8000/docs`.

### Auth

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/token` | Obtain JWT token |
| POST | `/api/v1/auth/register` | Register user (admin only) |

### Reports

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/reports` | Create report |
| GET | `/api/v1/reports` | List reports (paginated, filterable) |
| GET | `/api/v1/reports/{id}` | Get report by ID |
| PATCH | `/api/v1/reports/{id}` | Update report status/priority (admin) |
| DELETE | `/api/v1/reports/{id}` | Delete report (admin) |

### Filtering

```
GET /api/v1/reports?status=OPEN&priority=HIGH&reported_player=PlayerName&page=1&size=20
```

### Creating a report

```json
POST /api/v1/reports
{
  "reporter_name": "PlayerA",
  "reported_player": "PlayerB",
  "reason": "Hacking",
  "description": "Using aimbot in PvP near spawn.",
  "priority": "HIGH"
}
```

### Report status values

- `OPEN` — report received, pending review
- `REVIEWING` — staff is investigating
- `CLOSED` — resolved

### Priority values

- `LOW`, `MEDIUM`, `HIGH`

## Running tests

```bash
pip install aiosqlite
pytest --cov=app tests/
```

## Environment variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Async PostgreSQL URL | required |
| `SECRET_KEY` | JWT signing key | required |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry | `30` |
| `DEBUG` | Enable debug mode | `false` |
| `RATE_LIMIT_PER_MINUTE` | Requests per minute per IP | `60` |

## Author

**M4trixDev** — [github.com/m4trixdev](https://github.com/m4trixdev)

## License

MIT

