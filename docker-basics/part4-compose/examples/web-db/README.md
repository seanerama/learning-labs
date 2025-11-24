# Flask + PostgreSQL Example

A complete web application with Flask frontend and PostgreSQL database backend.

## Quick Start

```bash
# Start the application
docker compose up -d --build

# Test the application
curl http://localhost:5000

# Initialize database and track visits
curl http://localhost:5000/init

# View logs
docker compose logs -f web

# Stop and remove
docker compose down
```

## What It Demonstrates

- Web application connecting to database
- Service dependencies with health checks
- Data persistence with named volumes
- Container networking
- Environment-based configuration

## Endpoints

- `GET /` - Hello message
- `GET /health` - Health check
- `GET /init` - Initialize database and increment visit counter

## Architecture

```
┌──────────────┐
│  Flask Web   │  Port 5000
│  (Python)    │
└──────┬───────┘
       │ Connects via service name
       ▼
┌──────────────┐
│  PostgreSQL  │  Internal port 5432
│  Database    │
└──────────────┘
```

## Learn More

See the full lesson: [02-web-database.md](../../02-web-database.md)
