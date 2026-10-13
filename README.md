# AI Digital Bodyguard

[![CI](https://github.com/Pravinraje0761/AI_SECURITY_ASSISTANT/actions/workflows/ci.yml/badge.svg)](https://github.com/Pravinraje0761/AI_SECURITY_ASSISTANT/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A personal security assistant: a FastAPI service that scores URLs and emails for phishing and
scams, monitors processes, network connections and new files on the host, and raises alerts,
with a React dashboard, a desktop app and browser extensions as clients.

> **How detection works.** URL, email and file checks use transparent, rule-based feature
> scoring (`backend/app/ml/`): suspicious TLDs, look-alike domains, urgency language, and so on.
> No trained model is loaded. The model designs in `docs/design/` describe how ML classifiers
> would replace these rules.

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for local development)

### Using Docker (Recommended)

1. **Start the application:**
```bash
docker-compose up --build
```

2. **Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

3. **Register a user:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!","first_name":"Test","last_name":"User"}'
```

4. **Login to get token:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=Test123!"
```

5. **Test URL scanning:**
```bash
curl -X POST http://localhost:8000/api/v1/scan/url \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"phishing","target":"http://example.com"}'
```

### Local Development

#### Backend

1. **Install dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Set environment variables** (optional for local use; set `SECRET_KEY` anywhere shared):
```bash
cp .env.example .env
```

3. **Run the backend:**
```bash
python -m app.main
```

#### Frontend

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Run the frontend:**
```bash
npm run dev
```

## Components

| Folder | What it is |
|---|---|
| `backend/` | FastAPI service: auth (JWT), URL/email/file scanning, host monitoring, alerts |
| `frontend/` | React + Vite dashboard |
| `desktop/` | Desktop dashboard (launched by `start.py` / `launch_dashboard.pyw`) |
| `desktop_app/` | PyQt6 system-tray companion with notifications and auto-start |
| `browser_extensions/` | Chrome and Edge extension (full version) |
| `extensions/` | Simpler extension variant, including Firefox |
| `docs/design/` | Requirements, architecture and model design documents |

## API

| Area | Endpoints |
|---|---|
| Auth | `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `GET /api/v1/auth/me` |
| Scanning | `POST /api/v1/scan/url`, `GET /api/v1/scan/history` |
| Email & web protection | `POST /api/v1/protection/analyze-email`, `POST /api/v1/protection/check-url`, history endpoints |
| Host monitoring | `GET /api/v1/monitoring/{threat,score,resources,processes,connections,startup}`, `POST /api/v1/monitoring/scan-file` |
| Alerts | `GET /api/v1/alerts/`, acknowledge, counts, monitor start/stop |
| Health | `GET /health`, `GET /api/v1/dashboard` |

Interactive documentation: `http://localhost:8000/docs`.

## Tests

```bash
cd backend && pip install -r requirements.txt pytest && pytest
```

The tests run the API against a throwaway SQLite database: authentication, token checks,
URL and email scoring, and scan history. CI runs them and builds the dashboard on every push.

## Notes

- The application uses SQLite for simplicity in this demo
- Detection is rule-based (see the note at the top)
- For production, use PostgreSQL, set a strong `SECRET_KEY`, and replace the rules with trained models

## License

[MIT](LICENSE)
