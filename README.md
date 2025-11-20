# Learning Labs

A collection of hands-on learning guides and tutorials for network engineers and infrastructure professionals.

## Contents

### Kubernetes Learning Guide

**[kubernetes-learning-guide.md](kubernetes-learning-guide.md)** - Comprehensive guide to Kubernetes from a network engineer's perspective.

**Topics covered:**
- Docker and Kubernetes relationship
- Core Kubernetes concepts and networking
- Setting up Kubernetes with Docker Desktop on Windows 11/WSL2
- Example 1: Hello World with Nginx
- Example 2: FastAPI web application with PostgreSQL database
- Example 3: Multi-cluster deployment for geographic distribution
- Latency considerations and real-world architectures
- Troubleshooting commands and best practices

**Target Audience:** Network engineers, infrastructure professionals, and anyone looking to learn Kubernetes with a focus on networking concepts.

### FastAPI Demo Application

**[fastapi-demo/](fastapi-demo/)** - Complete example application used in the Kubernetes learning guide.

Includes:
- Python FastAPI application with PostgreSQL backend
- Dockerfile for containerization
- Kubernetes deployment manifests
- All configuration files

## Getting Started

1. Clone this repository:
   ```bash
   git clone https://github.com/seanerama/learning-labs.git
   cd learning-labs
   ```

2. Start with the Kubernetes Learning Guide:
   ```bash
   cat kubernetes-learning-guide.md
   ```

3. Follow along with the examples using the provided files in `fastapi-demo/`

## Contributing

Contributions are welcome! If you have learning materials, improvements, or corrections, please feel free to submit a pull request.

## License

MIT License - Feel free to use these materials for learning and teaching purposes.

---

**Maintained by:** [@seanerama](https://github.com/seanerama)
