# Lesson 2: Building Images

Master the docker build command and understand image management!

## 🎯 Objective

Learn advanced build techniques, image tagging, layer optimization, and how to manage your custom images effectively.

## 📝 What You'll Learn

- docker build command options
- Image tagging strategies
- Build context and .dockerignore
- Layer caching optimization
- Viewing image history
- Managing and cleaning up images

## 🚀 Steps

### Step 1: Basic Build with Tag

```bash
mkdir -p ~/docker-build-practice
cd ~/docker-build-practice

# Create simple Dockerfile
cat > Dockerfile << 'EOF'
FROM alpine:latest
RUN echo "Building my image..."
CMD ["echo", "Hello from custom image!"]
EOF

# Build with tag
docker build -t myapp:v1.0 .

# List images
docker images | grep myapp
```

Output:
```
REPOSITORY   TAG    IMAGE ID       CREATED         SIZE
myapp        v1.0   abc123def456   5 seconds ago   7.33MB
```

### Step 2: Multiple Tags

```bash
# Build with multiple tags at once
docker build -t myapp:v1.0 -t myapp:latest -t myapp:stable .

# List all tags
docker images | grep myapp
```

Output shows three tags pointing to same image:
```
myapp   v1.0     abc123def456   1 minute ago   7.33MB
myapp   latest   abc123def456   1 minute ago   7.33MB
myapp   stable   abc123def456   1 minute ago   7.33MB
```

### Step 3: Understanding Build Context

```bash
# Create some files
echo "Important file" > important.txt
echo "Secret file" > secret.txt
mkdir large-folder
dd if=/dev/zero of=large-folder/bigfile bs=1M count=100 2>/dev/null

# Build and watch what gets sent
docker build -t context-demo .
```

Notice: Docker sends ALL files in current directory!

```bash
# Create .dockerignore to exclude files
cat > .dockerignore << 'EOF'
secret.txt
large-folder/
*.log
**/__pycache__
.git
EOF

# Build again - much faster!
docker build -t context-demo .
```

### Step 4: Build with No Cache

```bash
# First build (uses cache)
time docker build -t cache-test .

# Build again (uses cache, very fast!)
time docker build -t cache-test .

# Build without cache (slower)
time docker build --no-cache -t cache-test .
```

### Step 5: Understanding Layer Cache

```bash
# Create Dockerfile that demonstrates caching
cat > Dockerfile << 'EOF'
FROM alpine:latest

# This layer rarely changes
RUN apk add --no-cache curl

# This changes often
COPY app.txt /app/app.txt

CMD ["cat", "/app/app.txt"]
EOF

# Create app file
echo "Version 1" > app.txt

# First build
docker build -t cache-demo .

# Change only app.txt
echo "Version 2" > app.txt

# Build again - RUN apk add is cached!
docker build -t cache-demo .
```

Output shows:
```
[1/3] FROM alpine:latest                CACHED
[2/3] RUN apk add --no-cache curl      CACHED
[3/3] COPY app.txt /app/app.txt        0.1s
```

### Step 6: Viewing Image History

```bash
# Build an image
cat > Dockerfile << 'EOF'
FROM alpine:latest
RUN apk add --no-cache curl vim
RUN mkdir -p /app/data
COPY app.txt /app/
CMD ["cat", "/app/app.txt"]
EOF

docker build -t history-demo .

# View image layers
docker history history-demo

# Or with more details
docker history --no-trunc history-demo
```

Output shows each layer with size:
```
IMAGE          CREATED         CREATED BY                                      SIZE
abc123...      5 seconds ago   CMD ["cat" "/app/app.txt"]                     0B
def456...      6 seconds ago   COPY app.txt /app/                              8B
ghi789...      10 seconds ago  RUN mkdir -p /app/data                          0B
jkl012...      12 seconds ago  RUN apk add --no-cache curl vim                 5.2MB
mno345...      3 weeks ago     /bin/sh -c #(nop)  CMD ["/bin/sh"]             0B
```

### Step 7: Build Arguments

```bash
# Dockerfile with ARG
cat > Dockerfile << 'EOF'
FROM alpine:latest

ARG APP_VERSION=1.0.0
ARG BUILD_DATE

RUN echo "Building version ${APP_VERSION} on ${BUILD_DATE}" > /version.txt

CMD ["cat", "/version.txt"]
EOF

# Build with custom arguments
docker build \
  --build-arg APP_VERSION=2.0.0 \
  --build-arg BUILD_DATE=$(date +%Y-%m-%d) \
  -t versioned-app .

# Run to see result
docker run --rm versioned-app
```

### Step 8: Different Dockerfile Names

```bash
# Create multiple Dockerfiles for different environments

# Development
cat > Dockerfile.dev << 'EOF'
FROM node:18
WORKDIR /app
ENV NODE_ENV=development
CMD ["npm", "run", "dev"]
EOF

# Production
cat > Dockerfile.prod << 'EOF'
FROM node:18-alpine
WORKDIR /app
ENV NODE_ENV=production
RUN npm install --production
CMD ["npm", "start"]
EOF

# Build using specific Dockerfile
docker build -f Dockerfile.dev -t myapp:dev .
docker build -f Dockerfile.prod -t myapp:prod .

# List both
docker images | grep myapp
```

### Step 9: Tagging Existing Images

```bash
# Build an image
docker build -t myapp:v1 .

# Add more tags to existing image
docker tag myapp:v1 myapp:latest
docker tag myapp:v1 myapp:production
docker tag myapp:v1 myregistry.com/myapp:v1

# List all tags
docker images | grep myapp
```

### Step 10: Image Cleanup

```bash
# Remove specific image
docker rmi myapp:v1

# Remove by ID
docker rmi abc123def456

# Remove unused images
docker image prune

# Remove all unused images (not just dangling)
docker image prune -a

# Remove images with specific pattern
docker images | grep 'myapp' | awk '{print $3}' | xargs docker rmi
```

## 🧪 Practical Scenarios

### Scenario 1: Optimized Python Image

```bash
mkdir -p ~/practice/python-optimized
cd ~/practice/python-optimized

# Create requirements
cat > requirements.txt << 'EOF'
flask==2.3.0
requests==2.31.0
EOF

# Create app
cat > app.py << 'EOF'
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello from optimized Python app!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF

# Optimized Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app.py .

# Don't run as root
RUN adduser --disabled-password --gecos '' appuser
USER appuser

EXPOSE 5000
CMD ["python", "app.py"]
EOF

# Build
docker build -t python-flask-optimized .

# Test
docker run -d -p 5000:5000 --name flask-app python-flask-optimized
sleep 2
curl http://localhost:5000
docker rm -f flask-app
```

### Scenario 2: Build Pipeline with Versioning

```bash
# Create versioning script
cat > build.sh << 'EOF'
#!/bin/bash

# Get version from git or increment
VERSION=${1:-1.0.0}
BUILD_DATE=$(date -u +%Y-%m-%dT%H:%M:%SZ)
GIT_COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "local")

echo "Building version $VERSION..."

docker build \
  --build-arg VERSION=$VERSION \
  --build-arg BUILD_DATE=$BUILD_DATE \
  --build-arg GIT_COMMIT=$GIT_COMMIT \
  -t myapp:$VERSION \
  -t myapp:latest \
  .

echo "Built: myapp:$VERSION and myapp:latest"
EOF

chmod +x build.sh

# Create Dockerfile that uses build args
cat > Dockerfile << 'EOF'
FROM alpine:latest

ARG VERSION=dev
ARG BUILD_DATE=unknown
ARG GIT_COMMIT=unknown

LABEL version="${VERSION}" \
      build-date="${BUILD_DATE}" \
      git-commit="${GIT_COMMIT}"

RUN echo "Version: ${VERSION}" > /version.txt && \
    echo "Build Date: ${BUILD_DATE}" >> /version.txt && \
    echo "Git Commit: ${GIT_COMMIT}" >> /version.txt

CMD ["cat", "/version.txt"]
EOF

# Build with version
./build.sh 2.0.0

# Check labels
docker inspect myapp:2.0.0 | grep -A 5 Labels
```

### Scenario 3: Multi-Architecture Build

```bash
# Build for multiple architectures (if buildx available)
# Note: This requires Docker Buildx

# Check if buildx is available
docker buildx version

# Create builder
docker buildx create --name multiarch --use

# Build for multiple platforms
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t myapp:multiarch \
  .

# Or build and push
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t myregistry.com/myapp:latest \
  --push \
  .
```

## 💡 Key Concepts

### Build Context

```
Build Context = Files sent to Docker daemon

Current Directory:
├── Dockerfile      ✅ Sent
├── app.py          ✅ Sent
├── .dockerignore   ✅ Read, controls what's sent
├── secret.env      ❌ Excluded by .dockerignore
└── node_modules/   ❌ Excluded by .dockerignore

Minimize build context:
- Use .dockerignore
- Don't put Dockerfile in directory with unnecessary files
- Use specific COPY commands
```

### .dockerignore Patterns

```.dockerignore
# Comments are allowed
**/*.log           # All log files
**/__pycache__     # Python cache dirs
.git               # Git directory
.gitignore         # Git ignore file
node_modules/      # Node modules
*.md               # Markdown files
!README.md         # Except README.md

# Environment files
.env
.env.*

# Build artifacts
dist/
build/
*.o
*.a
```

### Tagging Strategies

```bash
# Semantic versioning
myapp:1.0.0
myapp:1.0
myapp:1
myapp:latest

# Environment tags
myapp:dev
myapp:staging
myapp:production

# Date-based tags
myapp:2024-01-15
myapp:20240115

# Git-based tags
myapp:commit-abc123
myapp:branch-main

# Combination
myapp:v1.0.0-production
myapp:v1.0.0-20240115
```

### Layer Caching Rules

```
Cache is used if:
✅ Previous layer matches
✅ Instruction hasn't changed
✅ Files in COPY/ADD haven't changed

Cache is invalidated if:
❌ Base image updated
❌ Instruction changed
❌ Files in COPY changed
❌ Any previous layer changed

Example:
FROM alpine     ← Cache hit
RUN apk update  ← Cache hit (command same)
COPY app.py .   ← Cache miss (file changed)
RUN pip install ← Cache miss (previous layer changed)
```

### Image Size Optimization

```dockerfile
# Size comparison

# ❌ Large: 1.2GB
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y python3 python3-pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# ✅ Medium: 150MB
FROM python:3.11-slim
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# ✅ Small: 50MB (if using Alpine is appropriate)
FROM python:3.11-alpine
RUN apk add --no-cache gcc musl-dev
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```

## ✅ Practice Exercises

### Exercise 1: Build with Caching

Demonstrate layer caching:

<details>
<summary>Solution</summary>

```bash
mkdir -p ~/practice/caching
cd ~/practice/caching

# Create files
echo "flask==2.3.0" > requirements.txt
echo "print('Hello')" > app.py

# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim
WORKDIR /app

# These rarely change
COPY requirements.txt .
RUN pip install -r requirements.txt

# This changes often
COPY app.py .
CMD ["python", "app.py"]
EOF

# First build
time docker build -t cache-test .

# Modify only app.py
echo "print('Hello World!')" > app.py

# Second build - requirements installation is cached!
time docker build -t cache-test .

# Add new requirement
echo "requests==2.31.0" >> requirements.txt

# Third build - requirements layer rebuilds
time docker build -t cache-test .
```
</details>

### Exercise 2: Multi-Stage Preparation

Build an image with build-time dependencies:

<details>
<summary>Solution</summary>

```bash
mkdir -p ~/practice/build-deps
cd ~/practice/build-deps

cat > Dockerfile << 'EOF'
FROM python:3.11-slim

# Install build dependencies
RUN apt-get update && apt-get install -y gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app.py .

CMD ["python", "app.py"]
EOF

# Create requirements
cat > requirements.txt << 'EOF'
numpy==1.24.0
EOF

# Create app
cat > app.py << 'EOF'
import numpy as np
print(f"NumPy version: {np.__version__}")
print(f"Test array: {np.array([1, 2, 3])}")
EOF

docker build -t numpy-app .
docker run --rm numpy-app

# Note: Check image size
docker images | grep numpy-app
```
</details>

### Exercise 3: Version Management

Create a build system with proper versioning:

<details>
<summary>Solution</summary>

```bash
mkdir -p ~/practice/versioning
cd ~/practice/versioning

# Create app
cat > app.sh << 'EOF'
#!/bin/sh
cat /app/version.txt
echo "Application is running..."
EOF

# Create build script
cat > build.sh << 'EOF'
#!/bin/bash
set -e

VERSION=${1:-1.0.0}
BUILD_NUMBER=${BUILD_NUMBER:-local}

echo "Building version: $VERSION-$BUILD_NUMBER"

docker build \
  --build-arg VERSION=$VERSION \
  --build-arg BUILD=$BUILD_NUMBER \
  -t myapp:$VERSION \
  -t myapp:$VERSION-$BUILD_NUMBER \
  -t myapp:latest \
  .

echo "Tags created:"
echo "  - myapp:$VERSION"
echo "  - myapp:$VERSION-$BUILD_NUMBER"
echo "  - myapp:latest"
EOF

chmod +x build.sh

# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM alpine:latest

ARG VERSION=unknown
ARG BUILD=unknown

RUN echo "Version: $VERSION" > /app/version.txt && \
    echo "Build: $BUILD" >> /app/version.txt && \
    echo "Built at: $(date)" >> /app/version.txt

COPY app.sh /app/app.sh
RUN chmod +x /app/app.sh

CMD ["/app/app.sh"]
EOF

# Build with version
./build.sh 2.1.0

# Run
docker run --rm myapp:2.1.0
```
</details>

## 📊 Useful Commands

```bash
# Build with progress plain (shows all output)
docker build --progress=plain -t myapp .

# Build and remove intermediate containers
docker build --rm -t myapp .

# Build with specific target (multi-stage)
docker build --target production -t myapp .

# Show image digest
docker images --digests

# Export image to file
docker save myapp:latest -o myapp.tar

# Load image from file
docker load -i myapp.tar

# View image configuration
docker inspect myapp:latest

# Check image size breakdown
docker history --no-trunc --human myapp:latest

# Push to registry
docker push myregistry.com/myapp:latest

# Pull from registry
docker pull myregistry.com/myapp:latest
```

## ❓ Common Issues

### Issue: "failed to solve with frontend dockerfile.v0"

**Cause:** Syntax error in Dockerfile

**Solution:**
```bash
# Check Dockerfile syntax
cat Dockerfile

# Common errors:
# - Missing space after command
RUN echo"hello"  # ❌ Wrong
RUN echo "hello"  # ✅ Correct

# - Incorrect path
COPY file.txt /  # Missing filename
COPY file.txt /file.txt  # ✅ Correct
```

### Issue: Build is slow despite no changes

**Cause:** Cache not being used

**Check:**
```bash
# Is build context too large?
du -sh .

# Create/update .dockerignore
echo "node_modules" >> .dockerignore
echo ".git" >> .dockerignore

# Check for changing timestamps
# Don't use commands that change each build:
RUN date > /date.txt  # ❌ Always changes
```

### Issue: "no space left on device"

**Solution:**
```bash
# Check Docker disk usage
docker system df

# Clean up
docker system prune -a

# Remove unused images
docker image prune -a

# Remove build cache
docker builder prune
```

## 🎯 Best Practices

### 1. Use Specific Base Image Tags

```dockerfile
# ✅ GOOD - Reproducible
FROM python:3.11.5-slim

# ⚠️ OKAY - Less specific
FROM python:3.11-slim

# ❌ AVOID - Changes over time
FROM python:latest
```

### 2. Optimize Layer Order

```dockerfile
# ✅ GOOD - Stable layers first
FROM python:3.11-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# ❌ BAD - Code changes rebuild deps
FROM python:3.11-slim
COPY . .
RUN pip install -r requirements.txt
```

### 3. Combine RUN Commands

```dockerfile
# ✅ GOOD - One layer
RUN apt-get update && \
    apt-get install -y curl vim && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ❌ BAD - Multiple layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y vim
```

### 4. Use .dockerignore

```
# Always exclude:
.git
.gitignore
README.md
.env
*.log
__pycache__
node_modules
```

### 5. Tag Meaningfully

```bash
# ✅ GOOD - Semantic versioning
docker build -t myapp:v1.2.3 .

# ✅ GOOD - Include environment
docker build -t myapp:v1.2.3-prod .

# ❌ AVOID - Non-descriptive
docker build -t myapp:abc123 .
```

## 🎉 Lesson Complete!

You now know:

✅ Advanced docker build options
✅ Image tagging strategies
✅ Build context and .dockerignore
✅ Layer caching optimization
✅ Image history and inspection
✅ Image cleanup and management

### What's Next?

**Next Lesson:** [03 - Streamlit Hello World →](03-streamlit-hello.md)

Build a real web application with Streamlit and containerize it!

---

**Lesson Duration:** 20 minutes
**Difficulty:** Intermediate
**Prerequisites:** Lesson 1 completed
**Skills:** Image building, optimization, tagging
