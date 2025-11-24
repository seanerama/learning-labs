# Lesson 4: Docker Compose Commands

Master the docker compose command-line interface!

## 🎯 Essential Commands

### Starting and Stopping

```bash
# Start services
docker compose up                    # Foreground
docker compose up -d                 # Detached (background)
docker compose up --build           # Rebuild images first
docker compose up -d --scale web=3  # Scale service

# Stop services
docker compose stop                  # Stop (containers remain)
docker compose start                 # Start stopped containers
docker compose restart               # Restart services

# Remove services
docker compose down                  # Stop and remove
docker compose down -v              # Also remove volumes
docker compose down --rmi all       # Also remove images
```

### Viewing Status

```bash
# View running services
docker compose ps

# View all services (including stopped)
docker compose ps -a

# View logs
docker compose logs                  # All services
docker compose logs web             # Specific service
docker compose logs -f              # Follow logs
docker compose logs --tail=50       # Last 50 lines
docker compose logs -f --since 5m   # Last 5 minutes, follow
```

### Building and Images

```bash
# Build images
docker compose build                 # Build all
docker compose build web            # Build specific service
docker compose build --no-cache     # Force rebuild

# Pull images
docker compose pull                  # Pull all images
```

### Executing Commands

```bash
# Run command in running service
docker compose exec web sh
docker compose exec web ls /app
docker compose exec database psql -U postgres

# Run one-off command
docker compose run web python manage.py migrate
docker compose run --rm web pytest
```

### Configuration

```bash
# Validate compose file
docker compose config

# View merged configuration
docker compose config --services
docker compose config --volumes
```

## 📊 Quick Reference

```bash
# Most common workflow
docker compose up -d                 # Start
docker compose ps                    # Check status
docker compose logs -f web          # View logs
docker compose exec web sh          # Get shell
docker compose down                  # Stop and remove
```

## 🎉 Docker Basics Lab Complete!

Congratulations! You've completed all 4 parts and now know:

✅ Container basics and management
✅ Volumes, networks, and resource limits
✅ Building custom images with Dockerfiles
✅ Creating a Streamlit web application
✅ Multi-container orchestration with Compose

### Next Steps

- Deploy your own applications
- Explore Docker Swarm or Kubernetes
- Automate with CI/CD pipelines
- Learn about Docker security best practices

---

**Lesson Duration:** 5 minutes
**Difficulty:** Beginner
