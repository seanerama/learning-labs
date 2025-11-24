# Lesson 3: Multi-Tier Applications

Build complete application stacks with frontend, backend, and database!

## 🎯 Objective

Create a full-stack application with multiple tiers: frontend, API backend, database, and cache.

## 📝 Complete Example: 3-Tier App

```bash
mkdir -p ~/compose-apps/full-stack
cd ~/compose-apps/full-stack

cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  # Frontend - Nginx serving static files
  frontend:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./frontend:/usr/share/nginx/html:ro
    depends_on:
      - api
    networks:
      - frontend-net

  # Backend API - Python Flask
  api:
    image: python:3.11-alpine
    command: sh -c "pip install flask redis psycopg2-binary && python /app/api.py"
    volumes:
      - ./backend:/app
    environment:
      DB_HOST: database
      REDIS_HOST: cache
    depends_on:
      - database
      - cache
    networks:
      - frontend-net
      - backend-net

  # Database - PostgreSQL
  database:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: appdb
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - backend-net

  # Cache - Redis
  cache:
    image: redis:alpine
    networks:
      - backend-net

networks:
  frontend-net:    # Frontend <-> API
  backend-net:     # API <-> Database/Cache

volumes:
  db-data:
EOF

# Create frontend
mkdir frontend
cat > frontend/index.html << 'EOF'
<html>
<head><title>Multi-Tier App</title></head>
<body>
    <h1>Frontend</h1>
    <p>API is at: http://api:5000</p>
</body>
</html>
EOF

# Create backend
mkdir backend
cat > backend/api.py << 'EOF'
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/api/status')
def status():
    return jsonify({"status": "running", "tier": "backend"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF

docker compose up -d
docker compose ps
docker compose down
```

## 🎉 Lesson Complete!

✅ Multi-tier architecture
✅ Network segmentation
✅ Service orchestration

### What's Next?

**Next Lesson:** [04 - Compose Commands →](04-compose-commands.md)

---

**Lesson Duration:** 20 minutes
