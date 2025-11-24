# Docker Fundamentals Lab

A hands-on, progressive learning journey teaching Docker containerization from basics to multi-container applications.

## 🎯 Lab Overview

This lab provides a step-by-step guide to learn Docker through practical, hands-on examples. Starting with running pre-built containers, you'll progress to building your own images and orchestrating multi-container applications with Docker Compose.

### What You'll Build

By the end of this lab, you'll have:
- ✅ Run and managed containers from Docker Hub
- ✅ Built custom Docker images for Python applications
- ✅ Created a Streamlit web application in a container
- ✅ Deployed multi-container stacks with Docker Compose
- ✅ Understood container networking and persistence
- ✅ Applied production-ready container patterns

### Who This Lab Is For

- **Developers** wanting to containerize applications
- **Network Engineers** looking to run network tools in containers
- **DevOps Engineers** learning container orchestration
- **System Administrators** modernizing infrastructure
- **Students** learning cloud-native technologies

**No prior Docker experience required!** We teach everything from scratch.

## 🚀 Quick Start

### Prerequisites

- Docker installed (see [QUICKSTART.md](QUICKSTART.md))
- Basic command line knowledge
- Text editor (VS Code recommended)

### Get Started in 3 Steps

```bash
# 1. Clone the repository
git clone <repository-url>
cd learning-labs/docker-basics

# 2. Verify Docker installation
docker --version
docker run hello-world

# 3. Start learning
cat START-HERE.md
```

📖 **New to Docker?** Read [START-HERE.md](START-HERE.md) first!

⚡ **Need to install Docker?** Follow [QUICKSTART.md](QUICKSTART.md)

## 📚 Learning Path

This lab consists of 4 progressive parts:

---

### **Part 1: Container Basics**
**Concepts:** Pull, run, manage containers

Learn to work with pre-built containers from Docker Hub.

**What you'll learn:**
- How to find and pull images from Docker Hub
- Running containers in foreground and background
- Port mapping and accessing containerized services
- Accessing container shell (bash/sh)
- Viewing logs and inspecting containers
- Container lifecycle (start, stop, restart, remove)

**Hands-on examples:**
- Run a Speedtest server
- Deploy Nginx web server
- Access container shell
- View and follow logs

**Time:** 1 hour

```bash
cd part1-containers
cat README.md
```

---

### **Part 2: Container Management**
**Concepts:** Lifecycle, persistence, restart policies

Master container management for production use.

**What you'll learn:**
- Detached vs interactive modes
- Auto-restart policies (always, unless-stopped, on-failure)
- Environment variables in containers
- Volume mounting for data persistence
- Container networking basics
- Resource limits (CPU, memory)

**Hands-on examples:**
- Configure containers to start on boot
- Mount local directories into containers
- Pass environment variables
- Create and use Docker volumes
- Connect containers to networks

**Time:** 1 hour

```bash
cd part2-management
cat README.md
```

---

### **Part 3: Building Custom Images**
**Concepts:** Dockerfile, image building, best practices

Create your own container images.

**What you'll learn:**
- Dockerfile syntax and instructions
- Building images from Dockerfile
- Layer caching and optimization
- Multi-stage builds
- Image tagging and versioning
- Pushing to Docker Hub (optional)

**Hands-on projects:**
- Create a "Hello World" Streamlit app
- Write a Dockerfile for the app
- Build the Docker image
- Run your custom container
- Optimize image size

**Time:** 1.5 hours

```bash
cd part3-building
cat README.md
```

---

### **Part 4: Docker Compose**
**Concepts:** Multi-container applications, orchestration

Deploy applications with multiple connected containers.

**What you'll learn:**
- Docker Compose file syntax (YAML)
- Defining multi-container applications
- Container networking and service discovery
- Volume management in Compose
- Environment configuration
- Scaling services

**Hands-on projects:**
- Streamlit app + PostgreSQL database
- Network monitoring stack (Speedtest + Grafana)
- Multi-tier web application
- Development environment with hot-reload

**Time:** 1.5 hours

```bash
cd part4-compose
cat README.md
```

---

## 🎓 What You'll Learn

### Docker Fundamentals
- Container vs VM differences
- Docker architecture (client, daemon, registry)
- Images vs containers
- Container lifecycle
- Networking basics
- Storage and volumes

### Practical Skills
- Running pre-built containers
- Building custom images
- Writing Dockerfiles
- Using Docker Compose
- Debugging containers
- Security best practices

### Production Patterns
- Restart policies for reliability
- Data persistence strategies
- Multi-container orchestration
- Environment-based configuration
- Health checks
- Resource management

## 📁 Repository Structure

```
docker-basics/
├── part1-containers/              # Container basics
│   ├── README.md                  # Part 1 guide
│   ├── 01-hello-world.md          # First container
│   ├── 02-web-server.md           # Nginx example
│   ├── 03-speedtest.md            # Speedtest server
│   ├── 04-shell-access.md         # Container shell
│   └── 05-logs-inspect.md         # Debugging
│
├── part2-management/              # Container management
│   ├── README.md                  # Part 2 guide
│   ├── 01-restart-policies.md     # Boot on startup
│   ├── 02-environment-vars.md     # Configuration
│   ├── 03-volumes.md              # Data persistence
│   └── 04-networking.md           # Container networks
│
├── part3-building/                # Building images
│   ├── README.md                  # Part 3 guide
│   ├── streamlit-hello/           # Hello World app
│   │   ├── app.py                 # Streamlit application
│   │   ├── Dockerfile             # Image definition
│   │   ├── requirements.txt       # Python dependencies
│   │   └── README.md              # Build instructions
│   ├── 01-dockerfile-basics.md    # Dockerfile guide
│   ├── 02-building-images.md      # Build process
│   └── 03-optimization.md         # Best practices
│
├── part4-compose/                 # Docker Compose
│   ├── README.md                  # Part 4 guide
│   ├── simple-stack/              # Basic Compose example
│   │   ├── docker-compose.yml
│   │   └── README.md
│   ├── streamlit-postgres/        # App with database
│   │   ├── app/
│   │   │   ├── app.py
│   │   │   ├── Dockerfile
│   │   │   └── requirements.txt
│   │   ├── docker-compose.yml
│   │   └── README.md
│   └── monitoring-stack/          # Complete monitoring
│       ├── docker-compose.yml
│       └── README.md
│
├── examples/                      # Additional examples
│   └── network-tools/             # Network utility containers
│
├── .gitignore                     # Git ignore patterns
├── START-HERE.md                  # Entry point
├── QUICKSTART.md                  # Installation guide
└── README.md                      # This file
```

## 🛠️ Technology Stack

### Core Technologies
- **Docker** - Container platform
- **Docker Compose** - Multi-container orchestration
- **Docker Hub** - Container registry

### Example Applications
- **Streamlit** - Python web framework
- **PostgreSQL** - SQL database
- **Nginx** - Web server
- **Speedtest** - Network testing
- **Redis** - In-memory cache

### Supported Platforms
- ✅ **Linux** (native Docker)
- ✅ **macOS** (Docker Desktop)
- ✅ **Windows** (Docker Desktop with WSL 2)

## 🎯 Learning Progression

### Beginner Track (Parts 1-2)
Start here if you're new to Docker:
1. Run pre-built containers
2. Understand container basics
3. Learn management commands
4. Configure restart policies and volumes

**Time:** 2 hours

### Intermediate Track (Part 3)
Build your own images:
1. Understand Dockerfile syntax
2. Create custom images
3. Optimize builds
4. Deploy your applications

**Time:** 1.5 hours

### Advanced Track (Part 4)
Multi-container orchestration:
1. Docker Compose fundamentals
2. Container networking
3. Multi-tier applications
4. Production patterns

**Time:** 1.5 hours

**Total Lab Time:** 4-6 hours (self-paced)

## 💡 Usage Examples

### Example 1: Quick Web Server

```bash
# Pull and run Nginx
docker run -d -p 8080:80 --name my-web nginx

# Access at http://localhost:8080

# Stop and remove
docker stop my-web && docker rm my-web
```

### Example 2: Persistent Data

```bash
# Create a volume
docker volume create my-data

# Run container with volume
docker run -d -v my-data:/data --name my-app ubuntu

# Data persists even after container is removed
```

### Example 3: Multi-Container App

```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    build: ./app
    ports:
      - "8501:8501"
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
```

```bash
# Start entire stack
docker compose up -d

# Stop everything
docker compose down
```

## 🔒 Security Best Practices

This lab teaches secure container practices:

✅ **Don't run as root** - Use USER instruction in Dockerfile
✅ **Minimal base images** - Use alpine or distroless images
✅ **Scan for vulnerabilities** - Use `docker scan`
✅ **Limit resources** - Set CPU and memory limits
✅ **Use secrets** - Never hardcode passwords
✅ **Regular updates** - Keep images up to date
✅ **Network isolation** - Use custom networks

## 🧪 Use Cases Covered

### Development
- Local development environments
- Database testing
- API mocking
- Hot-reload workflows

### Testing
- Isolated test environments
- CI/CD pipelines
- Integration testing
- Reproducible builds

### Production
- Microservices deployment
- Web applications
- Databases and caches
- Monitoring stacks

### Network Engineering
- Network tools (speedtest, iperf)
- Automation platforms (Ansible AWX)
- Network monitoring (LibreNMS, Netbox)
- Lab environments

## 📖 Additional Resources

### Official Documentation
- [Docker Docs](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)

### Recommended Reading
- [Docker Deep Dive (Nigel Poulton)](https://www.amazon.com/Docker-Deep-Dive-Nigel-Poulton/dp/1521822808)
- [Docker in Action](https://www.manning.com/books/docker-in-action-second-edition)
- [Best Practices for Writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

### Community
- [Docker Community Forums](https://forums.docker.com/)
- [Docker Reddit](https://www.reddit.com/r/docker/)
- [Docker Discord](https://discord.gg/docker)

## 🤝 Real-World Applications

### For Network Engineers
```bash
# Run Speedtest server
docker run -d -p 8080:80 adolfintel/speedtest

# Run Network monitoring
docker run -d -p 3000:3000 grafana/grafana

# Run Ansible AWX
docker compose up  # See ansible-awx example
```

### For Developers
```bash
# Python development
docker run -it -v $(pwd):/app python:3.11 bash

# Node.js application
docker run -d -p 3000:3000 -v $(pwd):/app node:18

# Database for testing
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=test postgres:15
```

### For DevOps
```bash
# Jenkins CI/CD
docker run -d -p 8080:8080 jenkins/jenkins

# GitLab Runner
docker run -d --name gitlab-runner gitlab/gitlab-runner

# Monitoring stack
docker compose up -f monitoring/docker-compose.yml
```

## ❓ Troubleshooting

### Common Issues

**Container won't start:**
```bash
# Check logs for errors
docker logs <container-name>

# Run in foreground to see output
docker run <image>  # Without -d
```

**Port already in use:**
```bash
# Find what's using the port
docker ps
netstat -tulpn | grep <port>

# Use different port
docker run -p 8081:80 nginx
```

**Permission denied:**
```bash
# Add user to docker group (Linux)
sudo usermod -aG docker $USER
newgrp docker
```

**Out of disk space:**
```bash
# Clean up unused resources
docker system prune -a
docker volume prune
```

## 🎉 Ready to Start?

**Begin your journey:**
1. Read [START-HERE.md](START-HERE.md) for overview
2. Install Docker following [QUICKSTART.md](QUICKSTART.md)
3. Start with Part 1 - Container Basics

```bash
# Verify Docker is working
docker run hello-world

# Begin Part 1
cd part1-containers
cat README.md
```

---

**Platform:** Docker (Windows, Mac, Linux)
**Level:** Beginner to Intermediate
**Time:** 4-6 hours
**Prerequisites:** Basic command line knowledge

**What's Next:** After completing this lab, explore Kubernetes, Docker Swarm, or advanced container security!

**Happy Containerizing! 🐳**
