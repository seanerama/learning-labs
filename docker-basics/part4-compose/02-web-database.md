# Lesson 2: Web + Database

Build a complete application with web frontend and database backend working together!

## 🎯 Objective

Create a real-world multi-container application where a web service connects to a database, demonstrating how Docker Compose orchestrates multiple services.

## 📝 What You'll Learn

- Connecting web apps to databases
- Using depends_on for startup order
- Environment-based configuration
- Data persistence with volumes
- Health checks
- Complete application deployment

## 🚀 Complete Example: Flask + PostgreSQL

### Step 1: Create Project Structure

```bash
# Create project directory
mkdir -p ~/compose-apps/flask-postgres
cd ~/compose-apps/flask-postgres

# Create app directory
mkdir app
```

### Step 2: Create Python Flask Application

```bash
# Create Flask app that connects to PostgreSQL
cat > app/app.py << 'EOF'
from flask import Flask, jsonify
import psycopg2
import os
import time

app = Flask(__name__)

def get_db_connection():
    """Connect to PostgreSQL database"""
    max_retries = 5
    retry_count = 0

    while retry_count < max_retries:
        try:
            conn = psycopg2.connect(
                host=os.getenv('DB_HOST', 'database'),
                database=os.getenv('DB_NAME', 'myapp'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', 'secret')
            )
            return conn
        except psycopg2.OperationalError:
            retry_count += 1
            time.sleep(2)

    raise Exception("Could not connect to database")

@app.route('/')
def index():
    return jsonify({
        "message": "Hello from Flask!",
        "status": "running",
        "database": "connected"
    })

@app.route('/health')
def health():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "healthy"}), 200
    except:
        return jsonify({"status": "unhealthy"}), 500

@app.route('/init')
def init_db():
    """Initialize database with sample table"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Create table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS visits (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Insert visit
        cur.execute('INSERT INTO visits (timestamp) VALUES (CURRENT_TIMESTAMP)')

        # Get total visits
        cur.execute('SELECT COUNT(*) FROM visits')
        count = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "message": "Database initialized",
            "total_visits": count
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF
```

### Step 3: Create Requirements File

```bash
cat > app/requirements.txt << 'EOF'
flask==2.3.0
psycopg2-binary==2.9.9
EOF
```

### Step 4: Create Dockerfile

```bash
cat > app/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=10s --timeout=3s --start-period=40s \
  CMD python -c "import requests; requests.get('http://localhost:5000/health')" || exit 1

# Install curl for health check
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Run app
CMD ["python", "app.py"]
EOF
```

### Step 5: Create docker-compose.yml

```bash
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  # PostgreSQL Database
  database:
    image: postgres:15-alpine
    container_name: flask-postgres-db
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: secret
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  # Flask Web Application
  web:
    build: ./app
    container_name: flask-web
    ports:
      - "5000:5000"
    environment:
      DB_HOST: database
      DB_NAME: myapp
      DB_USER: postgres
      DB_PASSWORD: secret
    depends_on:
      database:
        condition: service_healthy
    networks:
      - app-network
    restart: unless-stopped

networks:
  app-network:
    driver: bridge

volumes:
  postgres-data:
EOF
```

### Step 6: Start the Application

```bash
# Build and start services
docker compose up -d --build

# This will:
# 1. Build Flask app image
# 2. Pull PostgreSQL image
# 3. Create network
# 4. Create volume
# 5. Start database
# 6. Wait for database to be healthy
# 7. Start web app
```

### Step 7: Test the Application

```bash
# Check services are running
docker compose ps

# Test web app
curl http://localhost:5000

# Initialize database
curl http://localhost:5000/init

# Check it again (visit count increases)
curl http://localhost:5000/init
```

### Step 8: View Logs

```bash
# View all logs
docker compose logs

# Follow web app logs
docker compose logs -f web

# View database logs
docker compose logs database
```

### Step 9: Access Database Directly

```bash
# Connect to PostgreSQL
docker compose exec database psql -U postgres -d myapp

# Inside PostgreSQL:
# \dt                    # List tables
# SELECT * FROM visits;  # View visits
# \q                     # Quit
```

### Step 10: Test Data Persistence

```bash
# Stop everything
docker compose down

# Start again (data persists!)
docker compose up -d

# Check visits are still there
curl http://localhost:5000/init
```

## 🧪 More Examples

### Example 2: Node.js + MongoDB

```bash
mkdir -p ~/compose-apps/node-mongo
cd ~/compose-apps/node-mongo

cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  mongo:
    image: mongo:7
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: secret
    volumes:
      - mongo-data:/data/db
    networks:
      - app-net

  app:
    image: node:18-alpine
    working_dir: /app
    command: sh -c "echo 'MongoDB URL: mongodb://admin:secret@mongo:27017' && sleep infinity"
    environment:
      MONGODB_URL: mongodb://admin:secret@mongo:27017
    depends_on:
      - mongo
    networks:
      - app-net

networks:
  app-net:

volumes:
  mongo-data:
EOF

docker compose up -d
docker compose logs app
docker compose down -v
```

### Example 3: Nginx + Redis

```bash
mkdir -p ~/compose-apps/nginx-redis
cd ~/compose-apps/nginx-redis

mkdir html
cat > html/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head><title>Nginx + Redis</title></head>
<body>
    <h1>Web Server Running</h1>
    <p>Redis is available at: redis:6379</p>
</body>
</html>
EOF

cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html:ro
    depends_on:
      - cache
    networks:
      - frontend

  cache:
    image: redis:alpine
    command: redis-server --requirepass mypassword
    networks:
      - frontend
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

networks:
  frontend:
EOF

docker compose up -d
curl http://localhost:8080

# Test Redis
docker compose exec cache redis-cli -a mypassword PING

docker compose down
```

## 💡 Key Concepts

### Service Dependencies

```yaml
services:
  web:
    depends_on:
      database:
        condition: service_healthy  # Wait for health check

  database:
    healthcheck:
      test: ["CMD", "pg_isready"]  # Health check command
```

### Environment Variables for Connection

```yaml
web:
  environment:
    DB_HOST: database        # Service name as hostname
    DB_PORT: 5432
    DB_NAME: myapp
```

### Volume Persistence

```yaml
services:
  database:
    volumes:
      - db-data:/var/lib/postgresql/data  # Named volume

volumes:
  db-data:  # Define named volume
```

### Network Isolation

```yaml
services:
  web:
    networks:
      - frontend
      - backend

  database:
    networks:
      - backend  # Not on frontend, isolated!

networks:
  frontend:
  backend:
```

## ✅ Practice Exercises

### Exercise 1: WordPress + MySQL

Create a complete WordPress site:

<details>
<summary>Solution</summary>

```bash
mkdir -p ~/practice/wordpress
cd ~/practice/wordpress

cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  wordpress:
    image: wordpress:latest
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress
      WORDPRESS_DB_NAME: wordpress
    volumes:
      - wordpress-data:/var/www/html
    depends_on:
      - db

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress
    volumes:
      - db-data:/var/lib/mysql

volumes:
  wordpress-data:
  db-data:
EOF

docker compose up -d
# Visit http://localhost:8080 to set up WordPress
docker compose down
```
</details>

### Exercise 2: Python API + Redis Cache

<details>
<summary>Solution</summary>

```bash
mkdir -p ~/practice/api-redis/app
cd ~/practice/api-redis

# Create simple API
cat > app/app.py << 'EOF'
from flask import Flask, jsonify
import redis
import os

app = Flask(__name__)
r = redis.Redis(
    host=os.getenv('REDIS_HOST', 'redis'),
    port=6379,
    decode_responses=True
)

@app.route('/count')
def count():
    count = r.incr('visits')
    return jsonify({"visits": count})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF

cat > app/requirements.txt << 'EOF'
flask==2.3.0
redis==5.0.1
EOF

cat > app/Dockerfile << 'EOF'
FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
EOF

cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  api:
    build: ./app
    ports:
      - "5000:5000"
    environment:
      REDIS_HOST: redis
    depends_on:
      - redis

  redis:
    image: redis:alpine

EOF

docker compose up -d --build
curl http://localhost:5000/count
curl http://localhost:5000/count
docker compose down
```
</details>

## 🎯 Best Practices

### 1. Use Health Checks

```yaml
database:
  healthcheck:
    test: ["CMD-SHELL", "pg_isready"]
    interval: 10s
    timeout: 5s
    retries: 5
```

### 2. Environment Files

```bash
# .env file
DB_PASSWORD=secret
DB_USER=admin

# docker-compose.yml
services:
  app:
    env_file: .env
```

### 3. Named Volumes for Data

```yaml
volumes:
  - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

### 4. Restart Policies

```yaml
services:
  web:
    restart: unless-stopped
```

## 🎉 Lesson Complete!

You now know:

✅ How to connect web apps to databases
✅ Service dependencies and health checks
✅ Data persistence with volumes
✅ Multi-container application deployment

### What's Next?

**Next Lesson:** [03 - Multi-Tier Applications →](03-multi-tier.md)

Build complete application stacks with frontend, API, and database!

---

**Lesson Duration:** 20 minutes
**Difficulty:** Intermediate
**Prerequisites:** Lesson 1 completed
**Skills:** Multi-container apps, database integration
