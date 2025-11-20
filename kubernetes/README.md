# Kubernetes Lab

Comprehensive guide to Kubernetes from a network engineer's perspective.

## Contents

- **[kubernetes-learning-guide.md](kubernetes-learning-guide.md)** - Complete learning guide
- **[fastapi-demo/](fastapi-demo/)** - Example application with all deployment files

## What You'll Learn

- Docker and Kubernetes relationship
- Core Kubernetes concepts and networking
- Setting up Kubernetes with Docker Desktop on Windows 11/WSL2
- Example 1: Hello World with Nginx
- Example 2: FastAPI web application with PostgreSQL database
- Example 3: Multi-cluster deployment for geographic distribution
- Latency considerations and real-world architectures
- Troubleshooting commands and best practices

## Prerequisites

- Windows 11 with WSL2
- Docker Desktop
- Basic understanding of networking concepts

## Quick Start

1. Read the complete guide:
   ```bash
   cat kubernetes-learning-guide.md
   ```

2. Follow along with the FastAPI demo:
   ```bash
   cd fastapi-demo
   docker build -t fastapi-demo:latest .
   kubectl apply -f postgres-deployment.yaml
   kubectl apply -f fastapi-deployment.yaml
   ```

## Target Audience

Network engineers, infrastructure professionals, and anyone looking to learn Kubernetes with a focus on networking concepts.
