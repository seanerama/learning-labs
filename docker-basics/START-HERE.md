# 🚀 START HERE - Docker Fundamentals Lab

## Welcome! 👋

Welcome to the **Docker Fundamentals Lab**! This hands-on learning path teaches you Docker from the ground up—from running your first container to building multi-container applications with Docker Compose.

## 📊 What You Have

This lab provides a **progressive learning journey** covering essential Docker skills:

- **4 comprehensive parts** from basics to advanced
- **Hands-on examples** with real applications
- **Progressive complexity** building on each concept
- **Production-ready patterns** you can use immediately
- **Real-world use cases** including Streamlit apps

## 🎯 Quick Navigation

### 🆕 New to Docker?
**Start here:** [QUICKSTART.md](QUICKSTART.md)
- 10-minute Docker installation
- Run your first container in 5 minutes
- No prior Docker experience needed

### 📚 Want the Full Learning Path?
**Read this:** [README.md](README.md)
- Complete 4-part curriculum
- What you'll learn in each part
- Best practices and patterns

### 🏗️ Need to Understand the Structure?
**Check out:** Lab structure overview below

## ⚡ 3-Minute Quick Start

```bash
# 1. Clone the learning labs repository
git clone <repository-url>
cd learning-labs/docker-basics

# 2. Verify Docker is installed
docker --version

# 3. Run your first container
docker run -d -p 8080:80 nginx
curl localhost:8080

# 4. Start learning!
cat part1-containers/README.md

# Done! 🎉
```

## 📁 What's Inside

```
docker-basics/
├── part1-containers/     # Docker basics, pull, run, shell access
├── part2-management/     # Lifecycle, restart policies, persistence
├── part3-building/       # Build custom images, Dockerfile
├── part4-compose/        # Multi-container apps with Compose
├── examples/             # Sample applications and configs
├── START-HERE.md         # This file
├── QUICKSTART.md         # Fast setup guide
└── README.md             # Complete overview
```

## 🎓 Learning Paths

### Path 1: Hands-On Learner (Recommended)
1. Install Docker (see QUICKSTART.md)
2. Work through Part 1-4 in order
3. Experiment with each example
4. Build your own containerized apps
5. Deploy multi-container stacks

### Path 2: Quick Start to Building
If you want to jump to building apps:
1. Review Part 1 basics (30 mins)
2. Jump to Part 3 - Building Images
3. Create your Streamlit app
4. Move to Part 4 - Docker Compose

### Path 3: Production Deployment Focus
For those deploying to production:
1. Complete Parts 1-2 for fundamentals
2. Focus on Part 2 - Management (restart policies, volumes)
3. Part 4 - Docker Compose for orchestration
4. Study networking and security sections

## 🔥 What You'll Learn

### Part 1: Container Basics (1 hour)
✅ Pull and run containers
✅ Port mapping and networking
✅ Access container shell
✅ View logs and inspect containers
✅ Container lifecycle management

### Part 2: Container Management (1 hour)
✅ Detached vs interactive mode
✅ Auto-restart policies (boot on startup)
✅ Environment variables
✅ Volume mounting and persistence
✅ Network configuration

### Part 3: Building Images (1.5 hours)
✅ Create a Streamlit Hello World app
✅ Write a Dockerfile
✅ Build custom images
✅ Multi-stage builds
✅ Image optimization
✅ Push to Docker Hub

### Part 4: Docker Compose (1.5 hours)
✅ Multi-container applications
✅ Docker Compose syntax
✅ Container communication
✅ Streamlit + Database stack
✅ Networking between containers
✅ Production patterns

**Total Lab Time:** 4-6 hours (self-paced)

## 🛠️ What You'll Build

### Example 1: Speedtest Server
Run a network speedtest server in a container:
- Pull public image
- Access via web browser
- Monitor performance
- Configure restart policies

### Example 2: Streamlit Hello World
Build your first containerized app:
- Simple Python web app
- Custom Dockerfile
- Port mapping
- Access from browser

### Example 3: Multi-Container Stack
Deploy connected services:
- Streamlit frontend
- PostgreSQL database
- Docker Compose orchestration
- Container networking

## 💡 Pro Tips

### Tip 1: Start Simple
Begin with public images before building your own. Understanding how containers work is crucial before creating them.

### Tip 2: Use Docker Desktop
Docker Desktop (Mac/Windows) provides a GUI and makes Docker easier to learn. Linux users use Docker Engine.

### Tip 3: Clean Up Regularly
```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove everything unused
docker system prune -a
```

### Tip 4: Check Logs Often
When things don't work, logs are your friend:
```bash
docker logs <container-name>
docker logs -f <container-name>  # Follow logs
```

### Tip 5: Use Docker Hub
Find pre-built images on [Docker Hub](https://hub.docker.com/) before building from scratch.

## ❓ Common Questions

**Q: Do I need to know Linux?**
A: Basic command line knowledge helps, but we explain everything as we go.

**Q: Can I use Windows?**
A: Yes! Docker Desktop works great on Windows, Mac, and Linux.

**Q: Do I need a powerful computer?**
A: No. Most examples run on any modern computer with 4GB+ RAM.

**Q: What's the difference between Docker and VMs?**
A: Containers share the host OS kernel (lightweight), VMs include full OS (heavy). We explain more in Part 1.

**Q: Is Docker only for developers?**
A: No! Network engineers, sysadmins, and DevOps engineers all use Docker for deploying applications and services.

**Q: Can I use this for network automation?**
A: Absolutely! Many network automation tools (Ansible AWX, Netbox, etc.) run in containers.

## 🆘 Need Help?

### Quick Fixes
```bash
# Docker not starting
sudo systemctl start docker  # Linux
# or restart Docker Desktop   # Mac/Windows

# Permission denied
sudo usermod -aG docker $USER  # Linux
# Then log out and back in

# Port already in use
docker ps  # Find conflicting container
docker stop <container>
```

### Documentation
- [QUICKSTART.md](QUICKSTART.md) - Installation and setup
- [README.md](README.md) - Complete learning path
- Part READMEs - Detailed instructions for each section

### External Resources
- [Docker Official Docs](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Docker Getting Started](https://www.docker.com/get-started)

## 🎯 Prerequisites

### Required
- Computer with 4GB+ RAM
- Internet connection
- Basic command line knowledge

### Nice to Have
- Text editor (VS Code recommended)
- Basic Python knowledge (for Streamlit example)
- Understanding of networking (ports, IPs)

## 🎉 You're Ready!

This lab will take you from Docker beginner to confident container user.

### Recommended First Steps:
1. 📖 Read [QUICKSTART.md](QUICKSTART.md) (10 mins)
2. 🏃 Install Docker (10 mins)
3. 🎮 Run your first container (5 mins)
4. 🎓 Continue through Parts 1-4

**Happy Containerizing! 🐳**

---

**Lab Level:** Beginner to Intermediate
**Time to Complete:** 4-6 hours
**Prerequisites:** Basic command line knowledge
**Platform:** Windows, Mac, Linux

**What's Next:** After this lab, explore Kubernetes, advanced networking, or container security!
