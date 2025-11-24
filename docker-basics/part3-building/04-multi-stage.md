# Lesson 4: Multi-Stage Builds

Dramatically reduce image size using multi-stage builds!

## 🎯 Objective

Learn how multi-stage builds work and how to use them to create smaller, more secure production images by separating build dependencies from runtime dependencies.

## 📝 What You'll Learn

- Understanding multi-stage builds
- Separating build and runtime environments
- Copying artifacts between stages
- Reducing image size
- Security benefits

## 🚀 Quick Example

### Problem: Large Image with Build Dependencies

```bash
mkdir -p ~/docker-multistage/before
cd ~/docker-multistage/before

# Create a Go application
cat > main.go << 'EOF'
package main
import "fmt"

func main() {
    fmt.Println("Hello from Go!")
}
EOF

# Single-stage Dockerfile (large!)
cat > Dockerfile << 'EOF'
FROM golang:1.21
WORKDIR /app
COPY main.go .
RUN go build -o myapp main.go
CMD ["./myapp"]
EOF

docker build -t go-app-large .
docker images | grep go-app-large
```

Result: **~800MB** (includes full Go SDK!)

### Solution: Multi-Stage Build

```bash
cd ~/docker-multistage
mkdir -p after
cd after

# Copy same Go file
cp ../before/main.go .

# Multi-stage Dockerfile (small!)
cat > Dockerfile << 'EOF'
# Stage 1: Build
FROM golang:1.21 AS builder
WORKDIR /app
COPY main.go .
RUN go build -o myapp main.go

# Stage 2: Runtime
FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/myapp .
CMD ["./myapp"]
EOF

docker build -t go-app-small .
docker images | grep go-app
```

Result: **~7MB** (only the binary!)

## 💡 Key Concepts

### Multi-Stage Syntax

```dockerfile
# Stage 1: Name it with "AS"
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Fresh start
FROM nginx:alpine
# Copy from previous stage
COPY --from=builder /app/dist /usr/share/nginx/html
```

### Benefits

- **Smaller images**: No build tools in final image
- **Faster deployments**: Less data to transfer
- **More secure**: Fewer attack vectors
- **Cleaner**: Only production dependencies

## ✅ Practice Exercises

### Exercise 1: Python with Compile Dependencies

```bash
mkdir -p ~/practice/python-multistage
cd ~/practice/python-multistage

cat > requirements.txt << 'EOF'
numpy==1.26.2
pandas==2.1.4
EOF

cat > app.py << 'EOF'
import numpy as np
import pandas as pd
print("NumPy version:", np.__version__)
print("Pandas version:", pd.__version__)
EOF

# Multi-stage Dockerfile
cat > Dockerfile << 'EOF'
# Build stage
FROM python:3.11 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app.py .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
EOF

docker build -t python-multistage .
docker run --rm python-multistage
```

### Exercise 2: Node.js React App

```bash
mkdir -p ~/practice/react-multistage
cd ~/practice/react-multistage

# Simplified React build
cat > Dockerfile << 'EOF'
# Build stage
FROM node:18 AS build
WORKDIR /app
# In real scenario: COPY package*.json and npm install
RUN echo "<h1>Built with Multi-Stage</h1>" > index.html

# Production stage
FROM nginx:alpine
COPY --from=build /app/index.html /usr/share/nginx/html/
EXPOSE 80
EOF

docker build -t react-app .
docker run -d -p 8080:80 --name react react-app
curl http://localhost:8080
docker rm -f react
```

## 🎉 Lesson Complete!

You now know how to:
✅ Use multi-stage builds
✅ Reduce image size dramatically
✅ Separate build and runtime dependencies
✅ Create production-ready images

### What's Next?

**Next Lesson:** [05 - Best Practices →](05-best-practices.md)

---

**Lesson Duration:** 15 minutes
**Difficulty:** Intermediate
**Prerequisites:** Lessons 1-3 completed
