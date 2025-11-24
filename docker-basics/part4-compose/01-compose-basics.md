# Lesson 1: Docker Compose Basics

Learn the fundamentals of Docker Compose and write your first docker-compose.yml!

## 🎯 Objective

Understand Docker Compose syntax, create your first multi-container application, and learn how Compose simplifies container orchestration.

## 📝 What You'll Learn

- docker-compose.yml structure
- Running multiple containers together
- Basic Compose commands
- Networking between containers
- Viewing logs and status

## 🚀 Steps

### Step 1: Simple Two-Container App

```bash
# Create project directory
mkdir -p ~/compose-basics/simple-app
cd ~/compose-basics/simple-app

# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"

  redis:
    image: redis:alpine
EOF
```

### Step 2: Start the Services

```bash
# Start all services in background
docker compose up -d

# View running services
docker compose ps
```

Output:
```
NAME           IMAGE          COMMAND                  STATUS    PORTS
simple-app-web-1      nginx:alpine  "nginx -g 'daemon of…"  Up        0.0.0.0:8080->80/tcp
simple-app-redis-1    redis:alpine  "docker-entrypoint.s…"  Up        6379/tcp
```

### Step 3: Test the Application

```bash
# Access Nginx
curl http://localhost:8080

# Check Redis is running
docker compose exec redis redis-cli ping
```

Output: `PONG`

### Step 4: View Logs

```bash
# View all logs
docker compose logs

# Follow logs for specific service
docker compose logs -f web

# Last 10 lines
docker compose logs --tail=10 redis
```

### Step 5: Stop and Remove

```bash
# Stop services (containers remain)
docker compose stop

# Start again
docker compose start

# Stop and remove everything
docker compose down
```

## 💡 Key Concepts

### docker-compose.yml Structure

```yaml
version: '3.8'              # Compose file format version

services:                   # Container definitions
  service-name:
    image: image:tag        # Use existing image
    # OR
    build: ./dir            # Build from Dockerfile

    ports:                  # Port mapping
      - "host:container"

    environment:            # Environment variables
      KEY: value

    volumes:                # Mount volumes
      - ./local:/container

    depends_on:             # Startup order
      - other-service

    networks:               # Networks to join
      - my-network

networks:                   # Network definitions
  my-network:

volumes:                    # Named volumes
  my-volume:
```

### Service Names = Hostnames

Containers can reach each other by service name:

```yaml
services:
  app:
    image: myapp
    environment:
      DATABASE_HOST: database  # Resolves to database container!

  database:
    image: postgres
```

## ✅ Practice Exercises

### Exercise 1: Web App with Custom HTML

```bash
mkdir -p ~/practice/custom-web
cd ~/practice/custom-web

# Create HTML file
mkdir html
echo "<h1>Hello from Docker Compose!</h1>" > html/index.html

# Create compose file
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html:ro
EOF

docker compose up -d
curl http://localhost:8080
docker compose down
```

### Exercise 2: App with Environment Variables

```bash
mkdir -p ~/practice/env-app
cd ~/practice/env-app

cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  app:
    image: alpine
    command: sh -c 'echo "App: $$APP_NAME v$$VERSION in $$ENVIRONMENT"'
    environment:
      APP_NAME: MyApp
      VERSION: 1.0.0
      ENVIRONMENT: production
EOF

docker compose up
docker compose down
```

## 🎉 Lesson Complete!

You now know:

✅ Basic docker-compose.yml syntax
✅ How to start/stop services
✅ Container networking with service names
✅ Viewing logs and status

### What's Next?

**Next Lesson:** [02 - Web + Database →](02-web-database.md)

Build a real application with frontend and database!

---

**Lesson Duration:** 15 minutes
**Difficulty:** Beginner
**Prerequisites:** Parts 1-3 completed
