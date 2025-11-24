# Part 3: Building Images

Learn to build your own Docker images from scratch!

## 🎯 Learning Objectives

By the end of this part, you'll be able to:
- ✅ Write Dockerfiles from scratch
- ✅ Build custom Docker images
- ✅ Understand image layers and caching
- ✅ Create a Streamlit web application
- ✅ Use multi-stage builds
- ✅ Optimize image sizes
- ✅ Tag and publish images

## 📚 Topics Covered

1. [Dockerfile Basics](01-dockerfile-basics.md) - First Dockerfile
2. [Building Images](02-building-images.md) - docker build command
3. [Streamlit Hello World](03-streamlit-hello.md) - Build a web app
4. [Multi-Stage Builds](04-multi-stage.md) - Optimize image size
5. [Image Best Practices](05-best-practices.md) - Production-ready images

## ⏱️ Time Estimate

**Total:** 1.5 hours
- Dockerfile Basics: 15 minutes
- Building Images: 20 minutes
- Streamlit Hello World: 30 minutes
- Multi-Stage Builds: 15 minutes
- Best Practices: 10 minutes

## 🚀 Getting Started

### Prerequisites

- Docker installed and running
- Completed Parts 1 & 2
- Basic understanding of running containers
- Text editor for writing Dockerfiles

### Verify You're Ready

```bash
# Can you run containers?
docker run --rm hello-world

# Can you view images?
docker images

# Do you have internet access? (for pulling base images)
docker pull alpine:latest
```

## 📖 Lessons

### Lesson 1: Dockerfile Basics

Learn the fundamentals of Dockerfile syntax and instructions.

[→ Go to Dockerfile Basics lesson](01-dockerfile-basics.md)

### Lesson 2: Building Images

Master the `docker build` command and understand image layers.

[→ Go to Building Images lesson](02-building-images.md)

### Lesson 3: Streamlit Hello World

Build a real web application with Streamlit and containerize it.

[→ Go to Streamlit Hello World lesson](03-streamlit-hello.md)

### Lesson 4: Multi-Stage Builds

Reduce image size dramatically using multi-stage builds.

[→ Go to Multi-Stage Builds lesson](04-multi-stage.md)

### Lesson 5: Image Best Practices

Learn production best practices for building secure, efficient images.

[→ Go to Best Practices lesson](05-best-practices.md)

## 🎓 Key Concepts

### What is a Dockerfile?

A Dockerfile is a **text file containing instructions** to build a Docker image. Think of it as a recipe:

```dockerfile
FROM ubuntu:22.04          # Start with base image
RUN apt-get update        # Run commands
COPY app.py /app/         # Copy files
CMD ["python", "app.py"]  # Define startup command
```

### Image Layers

```
┌─────────────────────────────────────────────┐
│         Image Layers                        │
├─────────────────────────────────────────────┤
│                                             │
│  Layer 5: CMD ["python", "app.py"]         │
│  Layer 4: COPY app.py /app/                │
│  Layer 3: RUN apt-get install python3      │
│  Layer 2: RUN apt-get update               │
│  Layer 1: FROM ubuntu:22.04                │
│                                             │
│  Each instruction creates a new layer!     │
└─────────────────────────────────────────────┘
```

### Build Process

```
Write Dockerfile → docker build → Image → docker run → Container
    ↓                  ↓            ↓          ↓           ↓
  Instructions      Build layers   Stored   Create     Running
                   and cache               instance    application
```

### Common Dockerfile Instructions

| Instruction | Purpose | Example |
|-------------|---------|---------|
| `FROM` | Base image | `FROM python:3.11` |
| `RUN` | Execute commands | `RUN pip install flask` |
| `COPY` | Copy files | `COPY app.py /app/` |
| `WORKDIR` | Set working directory | `WORKDIR /app` |
| `ENV` | Set environment variables | `ENV DEBUG=true` |
| `EXPOSE` | Document ports | `EXPOSE 8080` |
| `CMD` | Default command | `CMD ["python", "app.py"]` |
| `ENTRYPOINT` | Main executable | `ENTRYPOINT ["python"]` |

## 💡 Pro Tips

### Tip 1: Order Matters for Caching

```dockerfile
# ✅ GOOD - Dependencies cached, only code changes rebuild
FROM python:3.11
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .                          # Change here doesn't rebuild deps

# ❌ BAD - Any code change rebuilds everything
FROM python:3.11
COPY . .                               # Copies everything
RUN pip install -r requirements.txt    # Reinstalls every time
```

### Tip 2: Use Specific Tags

```dockerfile
# ✅ GOOD - Reproducible builds
FROM python:3.11-slim

# ❌ AVOID - :latest changes over time
FROM python:latest
```

### Tip 3: Minimize Layers

```dockerfile
# ✅ GOOD - Single layer for related commands
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean

# ❌ BAD - Multiple layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean
```

### Tip 4: Use .dockerignore

```bash
# Create .dockerignore to exclude files
cat > .dockerignore << EOF
__pycache__
*.pyc
.git
.env
node_modules
EOF
```

### Tip 5: Multi-Stage for Smaller Images

```dockerfile
# Build stage
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage - much smaller!
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

## 🎯 Practice Exercises

### Exercise 1: Simple Python App

Create a Dockerfile for a Python script:

```bash
# Create app
mkdir -p ~/docker-practice/python-app
cd ~/docker-practice/python-app

cat > app.py << 'EOF'
print("Hello from Docker!")
print("This is a containerized Python app")
EOF

# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-alpine
WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]
EOF

# Build and run
docker build -t my-python-app .
docker run --rm my-python-app
```

### Exercise 2: Web Server with Custom Page

Create a custom Nginx image:

```bash
mkdir -p ~/docker-practice/custom-web
cd ~/docker-practice/custom-web

# Create custom HTML
cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head><title>My Docker Site</title></head>
<body>
    <h1>Hello from My Custom Docker Image!</h1>
    <p>This page is served from a custom-built image.</p>
</body>
</html>
EOF

# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/
EXPOSE 80
EOF

# Build and run
docker build -t my-custom-nginx .
docker run -d -p 8080:80 my-custom-nginx

# Test
curl http://localhost:8080
```

### Exercise 3: Node.js Application

Build a Node.js app image:

```bash
mkdir -p ~/docker-practice/node-app
cd ~/docker-practice/node-app

# Create package.json
cat > package.json << 'EOF'
{
  "name": "docker-node-app",
  "version": "1.0.0",
  "main": "server.js",
  "dependencies": {
    "express": "^4.18.0"
  }
}
EOF

# Create server
cat > server.js << 'EOF'
const express = require('express');
const app = express();
const PORT = 3000;

app.get('/', (req, res) => {
  res.send('Hello from Dockerized Node.js!');
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
EOF

# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY server.js .
EXPOSE 3000
CMD ["node", "server.js"]
EOF

# Build and run
docker build -t my-node-app .
docker run -d -p 3000:3000 my-node-app

# Test
curl http://localhost:3000
```

## 🔍 Verification Checklist

Before moving to Part 4, ensure you can:

- [ ] Write a basic Dockerfile
- [ ] Build an image with `docker build`
- [ ] Understand how image layers work
- [ ] Use COPY, RUN, CMD instructions
- [ ] Set working directory with WORKDIR
- [ ] Build and run a Streamlit application
- [ ] Create multi-stage builds
- [ ] Optimize image sizes
- [ ] Tag images properly

## 📝 Quick Reference

```bash
# Build image from Dockerfile
docker build -t myimage:tag .

# Build from different file
docker build -t myimage -f Dockerfile.prod .

# Build with build args
docker build --build-arg VERSION=1.0 -t myimage .

# Build without cache
docker build --no-cache -t myimage .

# View image layers
docker history myimage

# View image details
docker inspect myimage

# Tag image
docker tag myimage:latest myimage:v1.0

# Remove image
docker rmi myimage

# Remove unused images
docker image prune
```

## ❓ Common Issues

### Issue: "COPY failed: no source files"

**Solution:**
```bash
# Make sure files exist
ls app.py

# Check .dockerignore isn't excluding them
cat .dockerignore

# Use correct path in COPY
COPY ./app.py /app/app.py
```

### Issue: Build is very slow

**Solution:**
```bash
# Use .dockerignore to exclude unnecessary files
echo "node_modules" >> .dockerignore
echo ".git" >> .dockerignore

# Order Dockerfile to maximize cache
# Put stable operations first, changing ones last
```

### Issue: Image is too large

**Solutions:**
```bash
# Use alpine base images
FROM python:3.11-alpine

# Use multi-stage builds
FROM builder AS build
# ... build steps ...
FROM alpine
COPY --from=build /app /app

# Clean up in same layer
RUN apt-get update && \
    apt-get install -y pkg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

## 🎯 Best Practices Summary

### 1. Always Use Specific Tags

```dockerfile
# ✅ GOOD
FROM python:3.11-slim

# ❌ AVOID
FROM python
```

### 2. Minimize Number of Layers

```dockerfile
# ✅ GOOD - One RUN command
RUN apt-get update && apt-get install -y \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# ❌ AVOID - Multiple RUN commands
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y vim
```

### 3. Use .dockerignore

```
# .dockerignore
**/__pycache__
**/*.pyc
.git
.env
*.md
tests/
```

### 4. Don't Run as Root

```dockerfile
# Create non-root user
RUN adduser -D appuser
USER appuser
```

### 5. Clean Up in Same Layer

```dockerfile
RUN apt-get update && \
    apt-get install -y pkg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

## 🎉 Part 3 Overview

After completing this part, you'll be able to:

✅ Write production-ready Dockerfiles
✅ Build custom images for any application
✅ Create a web application (Streamlit) from scratch
✅ Optimize images for size and performance
✅ Understand image layers and caching
✅ Use multi-stage builds

### What's Next?

**Next:** [Part 4 - Docker Compose →](../part4-compose/README.md)

In Part 4, you'll learn:
- Writing docker-compose.yml files
- Running multi-container applications
- Service orchestration
- Networking between services
- Volume management with Compose

---

**Time spent:** ~1.5 hours
**Skills gained:** Image building, Dockerfile authoring, application containerization
**Next step:** [Part 4 →](../part4-compose/README.md)
