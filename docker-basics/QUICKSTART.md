# Quick Start Guide - Docker Fundamentals

Get Docker installed and run your first container in 15 minutes!

## Prerequisites

Before you begin, ensure you have:

- ✅ Computer with 4GB+ RAM (8GB+ recommended)
- ✅ Internet connection
- ✅ Administrator/sudo access
- ✅ Basic command line knowledge

### System Requirements

**Windows:**
- Windows 10 64-bit: Pro, Enterprise, or Education (Build 19041 or higher)
- Or Windows 11
- WSL 2 feature enabled

**Mac:**
- macOS 10.15 or newer
- Apple Silicon or Intel processor

**Linux:**
- 64-bit distribution
- Kernel 3.10 or higher

## Installation Steps

### Option 1: Docker Desktop (Recommended for Windows/Mac)

#### Windows Installation

```powershell
# 1. Download Docker Desktop
# Visit: https://www.docker.com/products/docker-desktop

# 2. Run the installer
# Follow the installation wizard

# 3. Enable WSL 2 (if prompted)
wsl --install

# 4. Start Docker Desktop
# Use Start Menu or Desktop icon

# 5. Verify installation
docker --version
docker run hello-world
```

#### Mac Installation

```bash
# 1. Download Docker Desktop for Mac
# Visit: https://www.docker.com/products/docker-desktop

# 2. Drag Docker.app to Applications folder

# 3. Start Docker Desktop from Applications

# 4. Wait for Docker to start (whale icon in menu bar)

# 5. Verify installation
docker --version
docker run hello-world
```

### Option 2: Docker Engine (Linux)

#### Ubuntu/Debian

```bash
# 1. Update package index
sudo apt-get update

# 2. Install prerequisites
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# 3. Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
    sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 4. Set up the repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 6. Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# 7. Add your user to docker group (avoid sudo)
sudo usermod -aG docker $USER
newgrp docker  # Or log out and back in

# 8. Verify installation
docker --version
docker run hello-world
```

#### CentOS/RHEL/Fedora

```bash
# 1. Remove old versions (if any)
sudo yum remove docker docker-client docker-client-latest docker-common \
    docker-latest docker-latest-logrotate docker-logrotate docker-engine

# 2. Install yum-utils
sudo yum install -y yum-utils

# 3. Add Docker repository
sudo yum-config-manager \
    --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# 4. Install Docker Engine
sudo yum install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 5. Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# 6. Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# 7. Verify installation
docker --version
docker run hello-world
```

## Running Your First Container

### Test 1: Hello World

```bash
# Run the official hello-world container
docker run hello-world
```

**Expected Output:**
```
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

✅ **Success!** Docker is installed and working!

### Test 2: Nginx Web Server

```bash
# Run Nginx web server
docker run -d -p 8080:80 --name my-nginx nginx

# Check if it's running
docker ps

# Test in browser or with curl
curl http://localhost:8080
# Or open http://localhost:8080 in your browser

# View logs
docker logs my-nginx

# Stop the container
docker stop my-nginx

# Remove the container
docker rm my-nginx
```

### Test 3: Interactive Container

```bash
# Run Ubuntu container with interactive shell
docker run -it ubuntu bash

# Inside the container, try some commands
ls
pwd
cat /etc/os-release

# Exit the container
exit
```

## Quick Command Reference

```bash
# Container Management
docker ps                    # List running containers
docker ps -a                 # List all containers
docker run <image>           # Run a container
docker stop <container>      # Stop a container
docker start <container>     # Start a stopped container
docker rm <container>        # Remove a container
docker logs <container>      # View container logs

# Image Management
docker images                # List images
docker pull <image>          # Download an image
docker rmi <image>           # Remove an image
docker build -t <name> .     # Build an image from Dockerfile

# Docker Compose
docker compose up            # Start services
docker compose down          # Stop services
docker compose ps            # List services
docker compose logs          # View logs

# Cleanup
docker system prune          # Remove unused data
docker container prune       # Remove stopped containers
docker image prune           # Remove unused images
```

## Troubleshooting

### Issue: "docker: command not found"

**Solution (Linux):**
```bash
# Check if Docker service is running
sudo systemctl status docker

# Start Docker if stopped
sudo systemctl start docker
```

**Solution (Windows/Mac):**
- Ensure Docker Desktop is running
- Check system tray/menu bar for Docker icon
- Restart Docker Desktop

### Issue: "permission denied" (Linux)

**Solution:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and back in, or run:
newgrp docker

# Verify
docker ps
```

### Issue: Port already in use

**Solution:**
```bash
# Find container using the port
docker ps

# Stop the container
docker stop <container-name>

# Or use a different port
docker run -p 8081:80 nginx  # Use 8081 instead of 8080
```

### Issue: WSL 2 not installed (Windows)

**Solution:**
```powershell
# Run in PowerShell as Administrator
wsl --install

# Restart computer
# Then install Docker Desktop again
```

### Issue: Container won't start

**Solution:**
```bash
# Check logs for errors
docker logs <container-name>

# Check if port is available
netstat -an | grep <port>  # Linux/Mac
netstat -an | findstr <port>  # Windows

# Try running in foreground to see errors
docker run <image>  # Without -d flag
```

## Verify Installation Checklist

Run these commands to ensure everything works:

```bash
# 1. Check Docker version
docker --version
# Expected: Docker version 20.10.x or higher

# 2. Check Docker Compose
docker compose version
# Expected: Docker Compose version 2.x or higher

# 3. Run hello-world
docker run hello-world
# Expected: Success message

# 4. List images
docker images
# Expected: See hello-world image

# 5. Check Docker info
docker info
# Expected: Detailed Docker installation info
```

## Next Steps

Once Docker is installed and working:

1. ✅ **Read [START-HERE.md](START-HERE.md)** - Lab overview
2. ✅ **Read [README.md](README.md)** - Complete learning path
3. ✅ **Start Part 1** - Container basics
4. ✅ **Work through parts 2-4** - Build skills progressively

## Quick Start Example

Try this complete example:

```bash
# 1. Pull a Speedtest server image
docker pull adolfintel/speedtest

# 2. Run it
docker run -d -p 8080:80 --name speedtest adolfintel/speedtest

# 3. Access it in your browser
# Open: http://localhost:8080

# 4. Check logs
docker logs speedtest

# 5. Stop it
docker stop speedtest

# 6. Remove it
docker rm speedtest
```

## Docker Desktop Tips

### Windows/Mac Users

**Access Container Files:**
- Docker Desktop → Containers → Click container → Files tab

**View Logs:**
- Docker Desktop → Containers → Click container → Logs tab

**Resource Settings:**
- Docker Desktop → Settings → Resources
- Adjust CPU, Memory, Disk space

**Dashboard:**
- Monitor all containers visually
- Start/stop with one click
- Quick access to logs and shell

## Common First Commands

```bash
# See what's running
docker ps

# Run a web server
docker run -d -p 80:80 nginx

# Get a shell in a running container
docker exec -it <container-name> bash

# View all downloaded images
docker images

# Clean up everything
docker system prune -a
```

## Getting Help

### Built-in Help
```bash
docker --help                # General help
docker run --help            # Command-specific help
docker compose --help        # Compose help
```

### Documentation
- [Docker Docs](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Docker Forums](https://forums.docker.com/)

### This Lab
- [START-HERE.md](START-HERE.md) - Lab overview
- [README.md](README.md) - Complete guide
- Part READMEs - Detailed instructions

## Platform-Specific Notes

### Windows
- Use PowerShell or CMD
- WSL 2 provides better performance
- Can run Linux containers natively

### Mac
- Docker Desktop includes Kubernetes
- File sharing can be slow (use volumes)
- M1/M2 Macs use ARM architecture (some images may not work)

### Linux
- Native Docker performance
- No virtualization overhead
- Most flexible configuration

## Time Estimate

- **Installation:** 10-15 minutes
- **Verification:** 5 minutes
- **First containers:** 10 minutes
- **Total:** ~30 minutes

---

**You're now ready to start learning Docker!**

Proceed to [START-HERE.md](START-HERE.md) to begin your journey! 🐳

**Happy Containerizing! 🚀**
