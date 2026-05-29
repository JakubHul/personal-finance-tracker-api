# Personal Finance Tracker API

![CI](https://github.com/JakubHul/personal-finance-tracker-api/actions/workflows/ci.yml/badge.svg)

A FastAPI backend for tracking personal expenses with JWT authentication and per-user data isolation.

## Live API

**Base URL:** https://personal-finance-tracker-api-7zvy.onrender.com

Interaktywna dokumentacja (bez instalacji):
- **Swagger UI:** https://personal-finance-tracker-api-7zvy.onrender.com/docs
- **ReDoc:** https://personal-finance-tracker-api-7zvy.onrender.com/redoc

> ⚠️ Render Free tier zasypia po 15 minutach bezczynności. Pierwsze żądanie po uśpieniu może zająć ~30 sekund.

## Features

- User registration and login with JWT bearer tokens
- Per-user transaction CRUD with optional filters (category, amount, month, date range)
- Per-user budget management with ownership enforcement
- User-scoped statistics endpoint
- Database migrations with Alembic
- Dockerized — ready for deployment on Render / Railway

## Environment Variables

Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | ✅ | JWT signing secret — generate with `python -c "import secrets; print(secrets.token_hex(32))"` |
| `DATABASE_URL` | ✅ | e.g. `sqlite:///./finance.db` or `postgresql://user:pass@host/db` |
| `ALGORITHM` | optional | JWT algorithm, default `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | optional | Token lifetime, default `30` |

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# copy and fill .env
cp .env.example .env

# run database migrations
alembic upgrade head

# start the server
uvicorn app.main:app --reload
```

Interactive docs available at: http://127.0.0.1:8000/docs

## API Endpoints

### Auth
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/register` | — | Register new user |
| `POST` | `/login` | — | Login, returns JWT token |
| `GET` | `/me` | ✅ | Get current user ID |

### Transactions
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/transactions` | ✅ | Create transaction |
| `GET` | `/transactions` | ✅ | List own transactions (filterable) |
| `GET` | `/transactions/{id}` | ✅ | Get single transaction |
| `PUT` | `/transactions/{id}` | ✅ | Update transaction |
| `DELETE` | `/transactions/{id}` | ✅ | Delete transaction |

Query params for `GET /transactions`: `category`, `min_amount`, `max_amount`, `month` (YYYY-MM), `start_date`, `end_date`, `sort` (`asc`/`desc`)

### Budgets
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/budgets` | ✅ | Create budget |
| `GET` | `/budgets` | ✅ | List own budgets |
| `GET` | `/budgets/{id}` | ✅ | Get single budget |
| `PUT` | `/budgets/{id}` | ✅ | Update budget |
| `DELETE` | `/budgets/{id}` | ✅ | Delete budget |

### Stats
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/stats` | ✅ | Total expenses, count, max (optional `?month=YYYY-MM`) |

## Example Requests (Live API)

Możesz testować bezpośrednio — nie trzeba nic instalować lokalnie.

### Rejestracja
```bash
curl -X POST https://personal-finance-tracker-api-7zvy.onrender.com/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "mypassword"}'
```

### Login (zwraca token)
```bash
curl -X POST https://personal-finance-tracker-api-7zvy.onrender.com/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "mypassword"}'
```

### Dodaj transakcję
```bash
curl -X POST https://personal-finance-tracker-api-7zvy.onrender.com/transactions \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"amount": 150, "category": "food"}'
```

### Statystyki
```bash
curl "https://personal-finance-tracker-api-7zvy.onrender.com/stats?month=2026-05" \
  -H "Authorization: Bearer <TOKEN>"
```

## Example Requests (Local)

### Register
```bash
curl -X POST http://127.0.0.1:8000/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "mypassword"}'
```

### Login (returns token)
```bash
curl -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "mypassword"}'
```

### Add transaction
```bash
curl -X POST http://127.0.0.1:8000/transactions \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"amount": 150, "category": "food"}'
```

### Filter transactions
```bash
curl "http://127.0.0.1:8000/transactions?category=food&min_amount=50&month=2026-05" \
  -H "Authorization: Bearer <TOKEN>"
```

### Stats
```bash
curl "http://127.0.0.1:8000/stats?month=2026-05" \
  -H "Authorization: Bearer <TOKEN>"
```

## Database Migrations (Alembic)

```bash
# Apply all migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# Show current state
alembic current
```

## Running Tests

```bash
pytest tests/ -v
```

Tests use an in-memory SQLite database — no `.env` required.

## Docker

```bash
docker build -t personal-finance-api .
docker run -p 8000:8000 \
  -e SECRET_KEY=your-secret \
  -e DATABASE_URL=sqlite:///./finance.db \
  personal-finance-api
```

## Tech Stack

- **FastAPI** — web framework
- **SQLAlchemy 2** — ORM
- **Alembic** — database migrations
- **Pydantic v2 + pydantic-settings** — validation & config
- **python-jose** — JWT tokens
- **passlib + bcrypt** — password hashing
- **pytest + httpx** — testing
