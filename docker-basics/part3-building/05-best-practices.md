# Lesson 5: Image Best Practices

Build production-ready, secure, and efficient Docker images!

## 🎯 Objective

Learn industry best practices for creating Docker images that are secure, maintainable, and optimized for production use.

## 📝 Key Best Practices

### 1. Use Official Base Images

```dockerfile
# ✅ GOOD - Official, maintained
FROM python:3.11-slim
FROM node:18-alpine
FROM postgres:15

# ❌ AVOID - Unknown source
FROM random/python-image
```

### 2. Pin Specific Versions

```dockerfile
# ✅ BEST - Fully pinned
FROM python:3.11.5-slim

# ✅ GOOD - Minor version pinned
FROM python:3.11-slim

# ⚠️ OKAY - Major version only
FROM python:3-slim

# ❌ BAD - Changes over time
FROM python:latest
```

### 3. Minimize Layers

```dockerfile
# ✅ GOOD - Single layer
RUN apt-get update && \
    apt-get install -y \
        curl \
        vim \
        git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ❌ BAD - Multiple layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y vim
RUN apt-get install -y git
```

### 4. Order Instructions for Cache

```dockerfile
# ✅ GOOD - Stable first
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# ❌ BAD - Changes break cache
FROM python:3.11-slim
COPY . .
RUN pip install -r requirements.txt
```

### 5. Use .dockerignore

```
# Essential .dockerignore
**/__pycache__
**/*.pyc
.git
.env
*.log
node_modules/
.vscode/
.idea/
README.md
```

### 6. Don't Run as Root

```dockerfile
FROM python:3.11-slim

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser

# Set ownership
RUN mkdir /app && chown appuser:appuser /app
WORKDIR /app

# Switch to non-root
USER appuser

# Now runs as appuser
CMD ["python", "app.py"]
```

### 7. Use Multi-Stage Builds

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

### 8. Clean Up in Same Layer

```dockerfile
# ✅ GOOD - Clean in same RUN
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ❌ BAD - Cleanup doesn't reduce size
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean  # Too late, previous layers already large
```

### 9. Use COPY Instead of ADD

```dockerfile
# ✅ GOOD - Explicit copying
COPY app.py /app/

# ❌ AVOID - ADD has magic behavior
ADD app.py /app/

# ✅ EXCEPTION - When you need ADD features
ADD archive.tar.gz /app/  # Auto-extracts
```

### 10. Use Health Checks

```dockerfile
# Add health check for web apps
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD curl --fail http://localhost:8080/health || exit 1
```

### 11. Add Labels

```dockerfile
LABEL maintainer="you@example.com" \
      version="1.0.0" \
      description="My application" \
      org.opencontainers.image.source="https://github.com/user/repo"
```

### 12. Use Build Args for Flexibility

```dockerfile
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

ARG APP_ENV=production
ENV APP_ENV=${APP_ENV}
```

## ✅ Production-Ready Dockerfile Template

```dockerfile
# Multi-stage build for Python app
FROM python:3.11-slim AS builder

# Build arguments
ARG APP_VERSION=1.0.0

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim

# Metadata
LABEL maintainer="you@example.com" \
      version="${APP_VERSION}"

# Install runtime dependencies only
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application
COPY --chown=appuser:appuser app.py .

# Switch to non-root user
USER appuser

# Update PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl --fail http://localhost:8080/health || exit 1

# Expose port
EXPOSE 8080

# Run application
CMD ["python", "app.py"]
```

## 🎯 Security Checklist

- [ ] Use official base images
- [ ] Pin specific versions
- [ ] Scan for vulnerabilities (`docker scan`)
- [ ] Don't run as root
- [ ] Don't include secrets in image
- [ ] Use .dockerignore
- [ ] Minimize installed packages
- [ ] Keep base images updated
- [ ] Use multi-stage builds
- [ ] Add health checks

## 📊 Image Size Comparison

```bash
# Example progression
FROM ubuntu:22.04          # 77MB base
+ python3, pip             # +200MB = 277MB
+ dev dependencies         # +150MB = 427MB
+ app dependencies         # +100MB = 527MB
Total: ~527MB

# Optimized
FROM python:3.11-alpine    # 48MB base
+ app dependencies only    # +50MB = 98MB
Total: ~98MB (5x smaller!)
```

## 🎉 Part 3 Complete!

You now know:

✅ Dockerfile best practices
✅ Security considerations
✅ Optimization techniques
✅ Production-ready patterns

### What's Next?

**Next:** [Part 4 - Docker Compose →](../part4-compose/README.md)

Learn to orchestrate multiple containers with Docker Compose!

---

**Lesson Duration:** 10 minutes
**Difficulty:** Intermediate
**Prerequisites:** Lessons 1-4 completed
**Skills:** Production deployment, security, optimization
