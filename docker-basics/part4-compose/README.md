# Part 4: Docker Compose

Orchestrate multi-container applications with Docker Compose!

## 🎯 Learning Objectives

By the end of this part, you'll be able to:
- ✅ Write docker-compose.yml files
- ✅ Run multi-container applications
- ✅ Connect containers with networks
- ✅ Manage volumes with Compose
- ✅ Scale services
- ✅ Use environment files
- ✅ Deploy complete application stacks

## 📚 Topics Covered

1. [Compose Basics](01-compose-basics.md) - First docker-compose.yml
2. [Web + Database](02-web-database.md) - Two containers working together
3. [Multi-Tier Apps](03-multi-tier.md) - Full application stacks
4. [Compose Commands](04-compose-commands.md) - Managing services

## ⏱️ Time Estimate

**Total:** 1 hour
- Compose Basics: 15 minutes
- Web + Database: 20 minutes
- Multi-Tier Apps: 20 minutes
- Compose Commands: 5 minutes

## 🚀 Getting Started

### Prerequisites

- Docker Compose installed
- Completed Parts 1-3
- Basic understanding of networking and volumes

### Verify Docker Compose

```bash
# Check version
docker compose version

# Should show: Docker Compose version v2.x.x
```

## 📖 Lessons

### Lesson 1: Compose Basics

Learn the fundamentals of docker-compose.yml syntax.

[→ Go to Compose Basics lesson](01-compose-basics.md)

### Lesson 2: Web + Database

Create a web application with database backend.

[→ Go to Web + Database lesson](02-web-database.md)

### Lesson 3: Multi-Tier Applications

Build complete application stacks with frontend, backend, and database.

[→ Go to Multi-Tier Apps lesson](03-multi-tier.md)

### Lesson 4: Compose Commands

Master docker compose command-line operations.

[→ Go to Compose Commands lesson](04-compose-commands.md)

## 🎓 Key Concepts

### What is Docker Compose?

Docker Compose is a tool for defining and running multi-container Docker applications using a YAML file.

```yaml
version: '3.8'

services:
  web:
    image: nginx
    ports:
      - "80:80"

  database:
    image: postgres
    environment:
      POSTGRES_PASSWORD: secret
```

### Benefits

- **Single command deployment**: `docker compose up`
- **Service dependencies**: Automatic startup ordering
- **Network isolation**: Automatic network creation
- **Volume management**: Easy data persistence
- **Scaling**: Scale services up/down easily

### Basic Structure

```yaml
version: '3.8'             # Compose file version

services:                  # Define containers
  service1:
    image: nginx
    # service configuration

  service2:
    build: ./app
    # build from Dockerfile

networks:                  # Optional: custom networks
  my-network:

volumes:                   # Optional: named volumes
  my-data:
```

## 💡 Pro Tips

### Tip 1: Use Environment Files

```yaml
# docker-compose.yml
services:
  app:
    env_file:
      - .env
```

### Tip 2: Override for Different Environments

```bash
# Development
docker compose -f docker-compose.yml -f docker-compose.dev.yml up

# Production
docker compose -f docker-compose.yml -f docker-compose.prod.yml up
```

### Tip 3: Health Checks for Dependencies

```yaml
services:
  db:
    image: postgres
    healthcheck:
      test: ["CMD", "pg_isready"]

  app:
    depends_on:
      db:
        condition: service_healthy
```

### Tip 4: Use Named Volumes

```yaml
services:
  db:
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:  # Named volume
```

### Tip 5: Project Names

```bash
# Default: directory name
docker compose up

# Custom project name
docker compose -p myproject up

# Set via environment
export COMPOSE_PROJECT_NAME=myapp
docker compose up
```

## 🎯 Practice Exercises

### Exercise 1: Simple Web Stack

```yaml
version: '3.8'

services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html

  redis:
    image: redis:alpine
```

```bash
mkdir -p html
echo "<h1>Hello from Compose!</h1>" > html/index.html
docker compose up -d
curl http://localhost:8080
docker compose down
```

### Exercise 2: WordPress Site

```yaml
version: '3.8'

services:
  wordpress:
    image: wordpress:latest
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: secret
      WORDPRESS_DB_NAME: wordpress
    depends_on:
      - db

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootsecret
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: secret
    volumes:
      - db-data:/var/lib/mysql

volumes:
  db-data:
```

## 🔍 Verification Checklist

Before finishing, ensure you can:

- [ ] Write a basic docker-compose.yml
- [ ] Start services with `docker compose up`
- [ ] Connect containers on same network
- [ ] Use environment variables
- [ ] Persist data with volumes
- [ ] View service logs
- [ ] Scale services
- [ ] Stop and remove services

## 📝 Quick Reference

```bash
# Start services
docker compose up -d

# View status
docker compose ps

# View logs
docker compose logs -f

# Stop services
docker compose stop

# Remove services
docker compose down

# Remove with volumes
docker compose down -v

# Rebuild images
docker compose build

# Scale service
docker compose up -d --scale web=3

# Execute command in service
docker compose exec web sh
```

## ❓ Common Issues

### Issue: "service 'x' refers to undefined volume"

**Solution:**
```yaml
# Define the volume
volumes:
  my-volume:
```

### Issue: Port already in use

**Solution:**
```yaml
# Change host port
ports:
  - "8081:80"  # Instead of 8080
```

### Issue: Services can't communicate

**Solution:**
```yaml
# Use service names as hostnames
environment:
  DB_HOST: database  # Not localhost!
```

## 🎉 Part 4 Overview

After completing this part, you'll be able to:

✅ Define multi-container applications
✅ Manage service dependencies
✅ Configure networks and volumes
✅ Deploy complete application stacks
✅ Use Docker Compose in development and production

---

**Time spent:** ~1 hour
**Skills gained:** Multi-container orchestration, application stacks
**Next step:** Practice with real-world applications!
