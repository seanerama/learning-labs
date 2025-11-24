# Part 2: Container Management

Master container lifecycle, persistence, and advanced management techniques!

## 🎯 Learning Objectives

By the end of this part, you'll be able to:
- ✅ Configure containers to auto-start on system boot
- ✅ Use environment variables for configuration
- ✅ Persist data with volumes
- ✅ Configure container networking
- ✅ Set resource limits (CPU, memory)
- ✅ Manage container lifecycle effectively

## 📚 Topics Covered

1. [Restart Policies](01-restart-policies.md) - Auto-start containers
2. [Environment Variables](02-environment-vars.md) - Configure containers
3. [Volumes](03-volumes.md) - Data persistence
4. [Networking](04-networking.md) - Container communication
5. [Resource Limits](05-resource-limits.md) - Control CPU and memory

## ⏱️ Time Estimate

**Total:** 1.5 hours
- Restart Policies: 15 minutes
- Environment Variables: 20 minutes
- Volumes: 25 minutes
- Networking: 20 minutes
- Resource Limits: 10 minutes

## 🚀 Getting Started

### Prerequisites

- Docker installed and running
- Completed Part 1 (Container Basics)
- Basic understanding of running containers

### Verify You're Ready

```bash
# Can you run a container?
docker run --rm hello-world

# Can you access a web service?
docker run -d -p 8080:80 --name test nginx
curl http://localhost:8080
docker rm -f test
```

## 📖 Lessons

### Lesson 1: Restart Policies

Learn how to make containers automatically start on system boot and recover from failures.

[→ Go to Restart Policies lesson](01-restart-policies.md)

### Lesson 2: Environment Variables

Configure containers dynamically using environment variables instead of hard-coded values.

[→ Go to Environment Variables lesson](02-environment-vars.md)

### Lesson 3: Volumes

Persist data beyond container lifecycle with volumes. Essential for databases and stateful applications.

[→ Go to Volumes lesson](03-volumes.md)

### Lesson 4: Networking

Create custom networks, enable container-to-container communication, and understand Docker networking.

[→ Go to Networking lesson](04-networking.md)

### Lesson 5: Resource Limits

Control how much CPU and memory your containers can use to prevent resource exhaustion.

[→ Go to Resource Limits lesson](05-resource-limits.md)

## 🎓 Key Concepts

### Container Lifecycle Management

```
┌─────────────────────────────────────────┐
│         Container States                │
├─────────────────────────────────────────┤
│                                         │
│  Created → Running → Paused → Running  │
│              ↓                          │
│           Stopped → Restarting         │
│              ↓                          │
│           Removed                       │
└─────────────────────────────────────────┘
```

### Restart Policies

| Policy | Behavior |
|--------|----------|
| `no` | Don't restart (default) |
| `always` | Always restart, even after manual stop |
| `unless-stopped` | Restart unless manually stopped |
| `on-failure` | Restart only on error exit codes |

### Volume Types

```
┌─────────────────────────────────────────┐
│         Volume Types                    │
├─────────────────────────────────────────┤
│                                         │
│  Named Volumes    → docker volume create│
│  Bind Mounts      → -v /host:/container│
│  tmpfs Mounts     → --tmpfs (memory)   │
└─────────────────────────────────────────┘
```

### Network Modes

```
┌─────────────────────────────────────────┐
│         Network Modes                   │
├─────────────────────────────────────────┤
│                                         │
│  bridge    → Default, isolated network │
│  host      → Share host's network      │
│  none      → No networking             │
│  custom    → User-defined networks     │
└─────────────────────────────────────────┘
```

## 💡 Pro Tips

### Tip 1: Use unless-stopped for Services

```bash
# Best practice for services that should survive reboots
docker run -d --restart unless-stopped --name my-service nginx

# This allows you to manually stop it when needed
docker stop my-service  # Won't restart
```

### Tip 2: Named Volumes are Portable

```bash
# Named volumes can be backed up, migrated, shared
docker volume create my-data
docker run -v my-data:/app/data my-app

# List and inspect
docker volume ls
docker volume inspect my-data
```

### Tip 3: Environment Files

```bash
# Store env vars in a file
cat > .env << EOF
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
EOF

# Load them
docker run --env-file .env my-app
```

### Tip 4: Custom Networks Enable DNS

```bash
# On custom networks, containers can resolve each other by name
docker network create my-net
docker run -d --network my-net --name web nginx
docker run --network my-net alpine ping web  # Works!
```

### Tip 5: Resource Limits Prevent Runaway Containers

```bash
# Limit memory to 512MB, CPU to 50%
docker run -d \
  --memory="512m" \
  --cpus="0.5" \
  --name limited nginx
```

## 🎯 Practice Exercises

### Exercise 1: Persistent Web Server

Create an Nginx server that survives container recreation:

```bash
# Create volume
docker volume create web-data

# Run with volume
docker run -d \
  --name web \
  --restart unless-stopped \
  -p 8080:80 \
  -v web-data:/usr/share/nginx/html \
  nginx

# Add content
docker exec web sh -c 'echo "Hello from volume!" > /usr/share/nginx/html/index.html'

# Test
curl localhost:8080

# Recreate container - data persists!
docker rm -f web
docker run -d \
  --name web \
  -p 8080:80 \
  -v web-data:/usr/share/nginx/html \
  nginx

curl localhost:8080  # Still shows "Hello from volume!"
```

### Exercise 2: Multi-Container Communication

Create two containers that communicate on a custom network:

```bash
# Create network
docker network create app-net

# Run database
docker run -d \
  --name db \
  --network app-net \
  -e POSTGRES_PASSWORD=secret \
  postgres:alpine

# Run app that connects to db
docker run -it --rm \
  --network app-net \
  postgres:alpine \
  psql -h db -U postgres
# Password: secret
```

### Exercise 3: Resource-Limited Container

Run a container with strict resource limits:

```bash
# Create a container that tries to use lots of memory
docker run -d \
  --name limited \
  --memory="100m" \
  --memory-swap="100m" \
  --cpus="0.25" \
  nginx

# Monitor it
docker stats limited --no-stream
```

## 🔍 Verification Checklist

Before moving to Part 3, ensure you can:

- [ ] Configure a container to auto-start on boot
- [ ] Stop a container and prevent auto-restart
- [ ] Set environment variables with `-e` and `--env-file`
- [ ] Create and use named volumes
- [ ] Mount host directories into containers
- [ ] Create custom networks
- [ ] Connect containers to custom networks
- [ ] Set memory and CPU limits
- [ ] Verify resource usage with `docker stats`

## 📝 Quick Reference

```bash
# Restart policies
docker run -d --restart always nginx
docker run -d --restart unless-stopped nginx
docker run -d --restart on-failure:3 nginx
docker update --restart no my-container

# Environment variables
docker run -e KEY=value nginx
docker run --env-file .env nginx

# Volumes
docker volume create my-vol
docker run -v my-vol:/data nginx
docker run -v /host/path:/container/path nginx

# Networking
docker network create my-net
docker run --network my-net nginx
docker network connect my-net my-container

# Resource limits
docker run --memory="512m" --cpus="0.5" nginx
docker stats
docker update --memory="1g" my-container
```

## ❓ Common Issues

### Issue: Container doesn't restart on boot

**Possible causes:**
1. Docker daemon not set to start on boot
2. Wrong restart policy
3. Container exited with error

**Debug:**
```bash
# Check Docker service
sudo systemctl status docker
sudo systemctl enable docker

# Check container restart policy
docker inspect -f '{{.HostConfig.RestartPolicy}}' my-container

# Check container logs for errors
docker logs my-container
```

### Issue: Volume data disappeared

**Possible causes:**
1. Using anonymous volume instead of named volume
2. Mounted to wrong path
3. Volume was deleted

**Debug:**
```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect my-vol

# Check container mounts
docker inspect -f '{{.Mounts}}' my-container
```

### Issue: Containers can't communicate

**Possible causes:**
1. Not on same network
2. Using default bridge (no DNS)
3. Firewall rules

**Debug:**
```bash
# Check networks
docker network ls

# Check container network
docker inspect -f '{{.NetworkSettings.Networks}}' my-container

# Test connectivity
docker exec container1 ping container2
```

## 🎉 Part 2 Complete!

Congratulations! You've learned:

✅ Restart policies for production deployments
✅ Environment-based configuration
✅ Data persistence with volumes
✅ Container networking
✅ Resource management

### What's Next?

**Next:** [Part 3 - Building Images →](../part3-building/README.md)

In Part 3, you'll learn:
- Writing Dockerfiles
- Building custom images
- Multi-stage builds
- Creating a Streamlit application
- Optimizing image sizes
- Publishing to Docker Hub

---

**Time spent:** ~1.5 hours
**Skills gained:** Production container management
**Next step:** [Part 3 →](../part3-building/README.md)
