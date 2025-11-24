# Part 1: Container Basics

Welcome to Part 1! In this section, you'll learn the fundamentals of working with Docker containers.

## 🎯 Learning Objectives

By the end of this part, you'll be able to:
- ✅ Pull images from Docker Hub
- ✅ Run containers in different modes
- ✅ Map ports to access containerized services
- ✅ Access a container's shell
- ✅ View and follow container logs
- ✅ Manage container lifecycle (start, stop, restart, remove)
- ✅ Inspect container details

## 📚 Topics Covered

1. [Hello World](01-hello-world.md) - Your first container
2. [Web Server](02-web-server.md) - Running Nginx
3. [Speedtest Server](03-speedtest.md) - Real-world example
4. [Shell Access](04-shell-access.md) - Getting inside containers
5. [Logs & Inspect](05-logs-inspect.md) - Debugging containers

## ⏱️ Time Estimate

**Total:** 1 hour
- Hello World: 10 minutes
- Web Server: 15 minutes
- Speedtest Server: 15 minutes
- Shell Access: 10 minutes
- Logs & Inspect: 10 minutes

## 🚀 Getting Started

### Prerequisites

- Docker installed (see [../QUICKSTART.md](../QUICKSTART.md))
- Terminal/command prompt
- Internet connection

### Verify Docker Installation

```bash
# Check Docker version
docker --version

# Verify Docker is running
docker ps
```

Expected output:
```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

## 📖 Lessons

### Lesson 1: Hello World

Start with the simplest possible container to verify everything works.

[→ Go to Hello World lesson](01-hello-world.md)

### Lesson 2: Web Server

Run Nginx web server and access it from your browser.

[→ Go to Web Server lesson](02-web-server.md)

### Lesson 3: Speedtest Server

Deploy a real-world application - a network speedtest server.

[→ Go to Speedtest Server lesson](03-speedtest.md)

### Lesson 4: Shell Access

Learn how to get a shell inside running containers.

[→ Go to Shell Access lesson](04-shell-access.md)

### Lesson 5: Logs & Inspect

Debug containers using logs and inspect commands.

[→ Go to Logs & Inspect lesson](05-logs-inspect.md)

## 🎓 Key Concepts

### What is a Container?

A container is a **runnable instance of an image**. Think of:
- **Image** = Class (blueprint)
- **Container** = Object (running instance)

### Container vs Image

| Image | Container |
|-------|-----------|
| Static blueprint | Running instance |
| Stored on disk | Running in memory |
| Can't change | Can be modified |
| Template | Execution |

### Docker Architecture

```
┌─────────────────────────────────────────┐
│         Docker Client (CLI)             │
│         docker run, pull, etc.          │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│         Docker Daemon                   │
│         Manages containers/images       │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│         Docker Hub (Registry)           │
│         Public image repository         │
└─────────────────────────────────────────┘
```

### Common Commands

```bash
# Pull an image
docker pull <image>

# Run a container
docker run <options> <image>

# List running containers
docker ps

# List all containers
docker ps -a

# Stop a container
docker stop <container>

# Start a stopped container
docker start <container>

# Remove a container
docker rm <container>

# View logs
docker logs <container>

# Execute command in container
docker exec -it <container> <command>
```

## 💡 Pro Tips

### Tip 1: Name Your Containers

Always use `--name` to give containers meaningful names:
```bash
docker run --name my-web nginx
# Better than random names like "silly_darwin"
```

### Tip 2: Detached Mode

Use `-d` (detached) for services that should run in background:
```bash
docker run -d nginx  # Runs in background
docker run nginx     # Runs in foreground (blocks terminal)
```

### Tip 3: Port Mapping Format

Remember: `-p HOST:CONTAINER`
```bash
docker run -p 8080:80 nginx
# 8080 = Port on your computer
# 80 = Port inside container
```

### Tip 4: Clean Up Regularly

Stopped containers still take up disk space:
```bash
# Remove all stopped containers
docker container prune

# Remove specific container
docker rm <container-name>
```

### Tip 5: Use --rm for Temporary Containers

Auto-remove container when it stops:
```bash
docker run --rm ubuntu echo "Hello"
# Container is automatically deleted after running
```

## 🎯 Practice Exercises

Try these on your own:

### Exercise 1: Run Multiple Web Servers

Run two Nginx containers on different ports:
```bash
docker run -d -p 8080:80 --name web1 nginx
docker run -d -p 8081:80 --name web2 nginx

# Access both:
curl localhost:8080
curl localhost:8081
```

### Exercise 2: Container Lifecycle

Practice starting, stopping, and removing containers:
```bash
# Create and run
docker run -d --name test nginx

# Stop it
docker stop test

# Start it again
docker start test

# Remove it
docker stop test && docker rm test
```

### Exercise 3: Interactive Exploration

Run an interactive Ubuntu container:
```bash
docker run -it --rm ubuntu bash

# Inside container:
ls
pwd
cat /etc/os-release
exit
```

## 🔍 Verification Checklist

Before moving to Part 2, ensure you can:

- [ ] Pull an image from Docker Hub
- [ ] Run a container in detached mode
- [ ] Access a containerized service via browser
- [ ] List running and stopped containers
- [ ] Get a shell inside a container
- [ ] View container logs
- [ ] Stop and start containers
- [ ] Remove containers
- [ ] Map ports from host to container

## 📝 Quick Reference

```bash
# Essential commands for Part 1
docker pull nginx                # Download image
docker run -d -p 80:80 nginx     # Run container
docker ps                        # List running
docker ps -a                     # List all
docker stop <name>               # Stop container
docker start <name>              # Start container
docker rm <name>                 # Remove container
docker logs <name>               # View logs
docker exec -it <name> bash      # Get shell
docker inspect <name>            # Detailed info
```

## ❓ Common Issues

### Issue: "Cannot connect to Docker daemon"

**Solution:**
```bash
# Linux: Start Docker service
sudo systemctl start docker

# Mac/Windows: Start Docker Desktop
# Check system tray/menu bar
```

### Issue: "Port is already allocated"

**Solution:**
```bash
# Find container using the port
docker ps

# Stop it
docker stop <container-name>

# Or use a different port
docker run -p 8081:80 nginx
```

### Issue: "No such container"

**Solution:**
```bash
# List all containers
docker ps -a

# Container might have a different name
# Or was removed (use --rm flag)
```

## 🎉 Completion

Congratulations! You've completed Part 1.

You now understand:
- How to run containers from Docker Hub
- Port mapping and networking basics
- Container lifecycle management
- Basic debugging with logs

**Next:** [Part 2 - Container Management](../part2-management/README.md)

In Part 2, you'll learn about restart policies, volumes, environment variables, and more advanced container management techniques.

---

**Time spent:** ~1 hour
**Skills gained:** Docker basics, container operations
**Next step:** [Part 2 →](../part2-management/README.md)
