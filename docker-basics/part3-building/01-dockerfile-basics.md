# Lesson 1: Dockerfile Basics

Learn to write your first Dockerfile!

## 🎯 Objective

Understand Dockerfile syntax and create your first custom Docker image using basic instructions.

## 📝 What You'll Learn

- Dockerfile structure and syntax
- Common Dockerfile instructions (FROM, RUN, COPY, CMD)
- Layer concept and caching
- Building your first image
- Running containers from custom images

## 🚀 Steps

### Step 1: Your First Dockerfile

```bash
# Create a project directory
mkdir -p ~/docker-learning/first-image
cd ~/docker-learning/first-image

# Create a simple Dockerfile
cat > Dockerfile << 'EOF'
FROM alpine:latest
CMD ["echo", "Hello from my first Docker image!"]
EOF

# View the Dockerfile
cat Dockerfile
```

**Explanation:**
- `FROM alpine:latest` - Start with Alpine Linux (tiny base image)
- `CMD ["echo", "Hello..."]` - Command to run when container starts

### Step 2: Build the Image

```bash
# Build the image
docker build -t my-first-image .

# The dot (.) means "use current directory"
```

Output:
```
[+] Building 2.1s (5/5) FINISHED
 => [internal] load build definition from Dockerfile
 => => transferring dockerfile: 104B
 => [internal] load .dockerignore
 => [1/1] FROM docker.io/library/alpine:latest
 => exporting to image
 => => writing image sha256:abc123...
 => => naming to docker.io/library/my-first-image
```

### Step 3: View Your Image

```bash
# List images
docker images

# Should see:
# REPOSITORY         TAG       IMAGE ID       CREATED         SIZE
# my-first-image     latest    abc123def456   5 seconds ago   7.33MB
```

### Step 4: Run Your Image

```bash
# Run container from your image
docker run --rm my-first-image
```

Output:
```
Hello from my first Docker image!
```

**Success!** You built and ran your first custom image!

### Step 5: Adding More Instructions

```bash
# Create a more complex Dockerfile
cat > Dockerfile << 'EOF'
FROM alpine:latest

# RUN executes commands during build
RUN apk add --no-cache curl

# CMD runs when container starts
CMD ["curl", "--version"]
EOF

# Build with a new tag
docker build -t my-curl-image .

# Run it
docker run --rm my-curl-image
```

Output shows curl version information!

### Step 6: Copying Files Into Image

```bash
# Create a script
cat > hello.sh << 'EOF'
#!/bin/sh
echo "Hello from inside the container!"
echo "Current date: $(date)"
echo "Hostname: $(hostname)"
EOF

# Make it executable
chmod +x hello.sh

# Create Dockerfile that copies the script
cat > Dockerfile << 'EOF'
FROM alpine:latest

# Copy file from host to image
COPY hello.sh /usr/local/bin/hello.sh

# Make sure it's executable (in case chmod didn't work in build)
RUN chmod +x /usr/local/bin/hello.sh

# Run the script
CMD ["/usr/local/bin/hello.sh"]
EOF

# Build it
docker build -t hello-script .

# Run it
docker run --rm hello-script
```

### Step 7: Working Directory

```bash
# Create app files
mkdir app
echo "print('Hello from Python!')" > app/main.py

# Dockerfile with WORKDIR
cat > Dockerfile << 'EOF'
FROM python:3.11-alpine

# Set working directory
WORKDIR /app

# Copy files (destination is relative to WORKDIR)
COPY app/main.py .

# Run python script
CMD ["python", "main.py"]
EOF

# Build and run
docker build -t python-hello .
docker run --rm python-hello
```

**WORKDIR benefits:**
- Sets default directory for subsequent commands
- Creates directory if it doesn't exist
- All relative paths are from WORKDIR

### Step 8: Environment Variables

```bash
# Dockerfile with ENV
cat > Dockerfile << 'EOF'
FROM alpine:latest

# Set environment variables
ENV APP_NAME="MyApp" \
    APP_VERSION="1.0.0" \
    APP_ENV="production"

# Use env vars in CMD
CMD ["sh", "-c", "echo App: $APP_NAME v$APP_VERSION running in $APP_ENV"]
EOF

docker build -t env-demo .
docker run --rm env-demo
```

Output:
```
App: MyApp v1.0.0 running in production
```

### Step 9: EXPOSE Documentation

```bash
# Dockerfile with EXPOSE
cat > Dockerfile << 'EOF'
FROM nginx:alpine

# Document that this image uses port 80
EXPOSE 80

# Nginx starts automatically
EOF

docker build -t web-server .

# EXPOSE doesn't publish port, it's documentation
# Still need -p to actually map ports
docker run -d -p 8080:80 --name web web-server

curl http://localhost:8080

docker rm -f web
```

### Step 10: Multiple RUN Commands

```bash
# Create Dockerfile with multiple RUN commands
cat > Dockerfile << 'EOF'
FROM alpine:latest

# Each RUN creates a new layer
RUN echo "Layer 1: Installing packages"
RUN apk add --no-cache curl
RUN echo "Layer 2: Setting up directories"
RUN mkdir -p /app/data

# Check layers
CMD ["ls", "-la", "/app"]
EOF

docker build -t multi-layer .

# View image history (layers)
docker history multi-layer

# Run it
docker run --rm multi-layer
```

## 💡 Key Concepts

### Dockerfile Instruction Reference

```dockerfile
# FROM: Base image (required, usually first)
FROM ubuntu:22.04

# RUN: Execute commands during build
RUN apt-get update && apt-get install -y python3

# COPY: Copy files from host to image
COPY app.py /app/app.py

# ADD: Like COPY but can also extract tar files and download URLs
ADD archive.tar.gz /app/

# WORKDIR: Set working directory
WORKDIR /app

# ENV: Set environment variables
ENV DEBUG=true

# EXPOSE: Document which ports the container listens on
EXPOSE 8080

# CMD: Default command to run (can be overridden)
CMD ["python3", "app.py"]

# ENTRYPOINT: Main executable (harder to override)
ENTRYPOINT ["python3"]

# USER: Switch to non-root user
USER appuser

# VOLUME: Create mount point
VOLUME /data

# ARG: Build-time variables
ARG VERSION=1.0

# LABEL: Add metadata
LABEL maintainer="you@example.com"
```

### Instruction Timing

```
Build Time (docker build):
├─ FROM
├─ RUN
├─ COPY/ADD
├─ WORKDIR
├─ ENV
├─ ARG
└─ EXPOSE

Run Time (docker run):
├─ CMD
├─ ENTRYPOINT
└─ VOLUME (creates actual mount)
```

### COPY vs ADD

```dockerfile
# ✅ Use COPY for simple file copying
COPY app.py /app/

# ✅ Use ADD only when you need:
# - Extract tar files
ADD archive.tar.gz /app/  # Automatically extracts

# - Download from URL (but better to use RUN curl)
ADD https://example.com/file /app/

# Recommendation: Prefer COPY for clarity
```

### CMD vs ENTRYPOINT

```dockerfile
# CMD: Easy to override
FROM alpine
CMD ["echo", "hello"]
# docker run my-image           → echo hello
# docker run my-image echo bye  → echo bye (overridden!)

# ENTRYPOINT: Main command, harder to override
FROM alpine
ENTRYPOINT ["echo"]
CMD ["hello"]
# docker run my-image       → echo hello
# docker run my-image bye   → echo bye (CMD overridden, ENTRYPOINT stays)

# Use ENTRYPOINT for main executable
# Use CMD for default arguments
```

### Layer Caching

```
Docker caches each layer!

Dockerfile:
  FROM alpine        ← Layer 1 (cached)
  RUN apk update     ← Layer 2 (cached if no changes above)
  COPY app.py .      ← Layer 3 (rebuilds if app.py changed)
  RUN pip install    ← Layer 4 (rebuilds if Layer 3 rebuilt)

To maximize caching:
- Put stable instructions first
- Put frequently changing instructions last
```

## ✅ Practice Exercises

### Exercise 1: Static Website

Create a custom Nginx image with your own website:

<details>
<summary>Solution</summary>

```bash
mkdir -p ~/practice/static-site
cd ~/practice/static-site

# Create HTML files
mkdir website
cat > website/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head><title>My Docker Site</title></head>
<body>
    <h1>Welcome to My Dockerized Website!</h1>
    <p>This is served from a custom Docker image.</p>
</body>
</html>
EOF

# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM nginx:alpine
COPY website/ /usr/share/nginx/html/
EXPOSE 80
EOF

# Build and run
docker build -t my-website .
docker run -d -p 8080:80 --name site my-website

# Test
curl http://localhost:8080

# Clean up
docker rm -f site
```
</details>

### Exercise 2: Python Script with Dependencies

Create an image that runs a Python script with external packages:

<details>
<summary>Solution</summary>

```bash
mkdir -p ~/practice/python-deps
cd ~/practice/python-deps

# Create requirements file
cat > requirements.txt << 'EOF'
requests==2.31.0
EOF

# Create Python script
cat > app.py << 'EOF'
import requests
import json

response = requests.get('https://api.github.com')
print(f"GitHub API Status: {response.status_code}")
print(f"Rate Limit: {response.headers.get('X-RateLimit-Limit')}")
EOF

# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-alpine

WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY app.py .

CMD ["python", "app.py"]
EOF

# Build and run
docker build -t python-requests .
docker run --rm python-requests
```
</details>

### Exercise 3: Multi-Command Setup

Create an image that sets up a complete environment:

<details>
<summary>Solution</summary>

```bash
mkdir -p ~/practice/setup-env
cd ~/practice/setup-env

cat > Dockerfile << 'EOF'
FROM alpine:latest

# Install multiple packages in one layer
RUN apk add --no-cache \
    curl \
    git \
    vim \
    bash

# Create directories
RUN mkdir -p /app/data /app/logs

# Set environment
ENV APP_HOME=/app \
    PATH="/app/bin:$PATH"

# Set working directory
WORKDIR /app

# Create a startup script
RUN echo '#!/bin/bash' > /app/startup.sh && \
    echo 'echo "Environment ready!"' >> /app/startup.sh && \
    echo 'echo "App home: $APP_HOME"' >> /app/startup.sh && \
    echo 'ls -la /app' >> /app/startup.sh && \
    chmod +x /app/startup.sh

CMD ["/app/startup.sh"]
EOF

docker build -t setup-env .
docker run --rm setup-env
```
</details>

## 🔧 Advanced Usage

### Build Arguments

```bash
# Dockerfile with ARG
cat > Dockerfile << 'EOF'
FROM alpine:latest

# Define build argument
ARG VERSION=1.0.0

# Use in RUN (only available during build)
RUN echo "Building version $VERSION" > /version.txt

CMD ["cat", "/version.txt"]
EOF

# Build with default
docker build -t app:default .
docker run --rm app:default

# Build with custom value
docker build --build-arg VERSION=2.0.0 -t app:v2 .
docker run --rm app:v2
```

### Health Checks

```dockerfile
FROM nginx:alpine

# Add health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

EXPOSE 80
```

### Labels for Metadata

```dockerfile
FROM alpine:latest

LABEL maintainer="you@example.com" \
      version="1.0" \
      description="My custom image"

CMD ["echo", "Hello"]
```

### User Security

```dockerfile
FROM alpine:latest

# Create non-root user
RUN addgroup -g 1000 appgroup && \
    adduser -D -u 1000 -G appgroup appuser

# Create app directory
RUN mkdir /app && chown appuser:appgroup /app

# Switch to non-root user
USER appuser

WORKDIR /app
CMD ["sh"]
```

## 📊 Useful One-Liners

```bash
# Build with no cache
docker build --no-cache -t myimage .

# Build and tag multiple times
docker build -t myimage:latest -t myimage:v1.0 .

# Build from stdin
cat Dockerfile | docker build -t myimage -

# Build with different Dockerfile name
docker build -f Dockerfile.prod -t myimage .

# Show build process in detail
docker build --progress=plain -t myimage .

# Build and immediately run
docker build -t myimage . && docker run --rm myimage

# View image layers and sizes
docker history myimage

# View detailed image info
docker inspect myimage
```

## ❓ Common Issues

### Issue: "COPY failed: stat: no such file"

**Cause:** File doesn't exist or wrong path

**Solution:**
```bash
# Check file exists
ls -la app.py

# Make sure Docker can see it (not in .dockerignore)
cat .dockerignore

# Use correct relative path in Dockerfile
COPY ./app.py /app/
```

### Issue: Build is slow / downloads every time

**Cause:** Not using cache effectively

**Solution:**
```dockerfile
# ❌ BAD: Changes to app.py rebuild everything
FROM python:3.11
COPY . .
RUN pip install -r requirements.txt

# ✅ GOOD: Only rebuild pip install if requirements change
FROM python:3.11
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

### Issue: Permission denied when running

**Cause:** Files not executable or wrong ownership

**Solution:**
```dockerfile
# Make file executable
COPY script.sh /app/
RUN chmod +x /app/script.sh

# Or set ownership
RUN chown -R appuser:appuser /app
USER appuser
```

## 🎯 Best Practices

### 1. Use Official Base Images

```dockerfile
# ✅ GOOD
FROM python:3.11-slim

# ❌ AVOID
FROM random-python-image
```

### 2. Pin Specific Versions

```dockerfile
# ✅ GOOD
FROM python:3.11.5-slim

# ⚠️ OKAY
FROM python:3.11-slim

# ❌ AVOID
FROM python
```

### 3. Minimize Layers

```dockerfile
# ✅ GOOD
RUN apt-get update && \
    apt-get install -y curl vim && \
    apt-get clean

# ❌ AVOID
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y vim
RUN apt-get clean
```

### 4. Order Instructions for Cache

```dockerfile
# ✅ GOOD: Stable first, volatile last
FROM python:3.11
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# ❌ BAD: Changes to code rebuild everything
FROM python:3.11
COPY . .
RUN pip install -r requirements.txt
```

### 5. Use .dockerignore

```bash
# Create .dockerignore
cat > .dockerignore << 'EOF'
**/__pycache__
**/*.pyc
.git
.gitignore
README.md
.env
*.log
EOF
```

## 🎉 Lesson Complete!

You now know:

✅ Basic Dockerfile syntax and structure
✅ Common instructions (FROM, RUN, COPY, CMD)
✅ How to build images with docker build
✅ How layers and caching work
✅ Best practices for writing Dockerfiles

### What's Next?

**Next Lesson:** [02 - Building Images →](02-building-images.md)

Dive deeper into the build process, image tagging, and optimization!

---

**Lesson Duration:** 15 minutes
**Difficulty:** Beginner
**Prerequisites:** Part 1-2 completed
**Skills:** Dockerfile authoring, image building
