# AI Digital Bodyguard - Working Application

A working implementation of the AI-Powered Digital Bodyguard for cyber threat detection.

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

2. **Set environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
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

## Features Implemented

- ✅ User authentication (register/login)
- ✅ JWT token-based authentication
- ✅ Phishing URL detection
- ✅ React frontend with routing
- ✅ SQLite database
- ✅ Docker deployment

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user info

### Scanning
- `POST /api/v1/scan/url` - Scan URL for phishing

### Health
- `GET /health` - Health check

## Project Structure

```
ai_security assisatajt/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   ├── utils/        # Utilities
│   │   ├── config.py     # Configuration
│   │   ├── database.py   # Database setup
│   │   └── main.py       # FastAPI app
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── pages/        # React pages
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── Dockerfile
│   └── index.html
└── docker-compose.yml
```

## Notes

- TypeScript lint errors in the frontend are expected until `npm install` is run
- The application uses SQLite for simplicity in this demo
- The phishing detection uses a simple rule-based approach for demonstration
- For production, use PostgreSQL and implement the full ML models from the documentation
