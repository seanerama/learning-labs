# Containerlab - Quick Start Installation Guide

Get Containerlab up and running in minutes.

## Prerequisites

- Linux system (Ubuntu 20.04+, Debian 11+, RHEL 8+, or similar)
- Root or sudo access
- Internet connection

## Step 1: Install Docker

Containerlab uses Docker to run containers. If you already have Docker installed, skip to Step 2.

### Ubuntu / Debian

```bash
# Update package index
sudo apt update

# Install using the convenience script
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Verify installation
docker --version
```

### RHEL / CentOS / Fedora

```bash
# Install using the convenience script
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Verify installation
docker --version
```

### Verify Docker is Running

```bash
sudo docker run hello-world
```

You should see a "Hello from Docker!" message.

## Step 2: Install Containerlab

```bash
# Download and install Containerlab
bash -c "$(curl -sL https://get.containerlab.dev)"

# Verify installation
containerlab version
```

**Expected output:**
```
                           _                   _       _
                 _        (_)                 | |     | |
 ____ ___  ____ | |_  ____ _ ____   ____  ____| | ____| | _
/ ___) _ \|  _ \|  _)/ _  | |  _ \ / _  )/ ___) |/ _  | || \
( (__| |_|| | | | |_( ( | | | | | ( (/ /| |   | ( ( | | |_) )
\____)___/|_| |_|\___)_||_|_|_| |_|\____)_|   |_|\_||_|____/

version: 0.xx.x
```

## Step 3: Verify Setup

```bash
# Check Docker
sudo docker ps

# Check Containerlab
containerlab version

# Pull the Alpine image (used in our lab)
sudo docker pull alpine:latest
```

## Step 4: Deploy Test Lab

Navigate to the containerlab directory and deploy:

```bash
cd /path/to/learning-labs/containerlab

# Deploy the lab
sudo containerlab deploy -t simple-lab.clab.yml

# Verify containers are running
sudo docker ps
```

**Expected output:**
```
CONTAINER ID   IMAGE           COMMAND   CREATED         STATUS         NAMES
abc123...      alpine:latest   ...       5 seconds ago   Up 4 seconds   clab-simple-lab-client1
def456...      alpine:latest   ...       5 seconds ago   Up 4 seconds   clab-simple-lab-router
ghi789...      alpine:latest   ...       5 seconds ago   Up 4 seconds   clab-simple-lab-server1
```

## Step 5: Test Connectivity

```bash
# Access the client container
sudo docker exec -it clab-simple-lab-client1 sh

# Inside the container, ping the router
ping -c 3 192.168.1.1

# Exit the container
exit
```

If ping succeeds, your lab is working!

## Cleanup

When done testing:

```bash
sudo containerlab destroy -t simple-lab.clab.yml
```

## Troubleshooting

### "command not found: containerlab"

The installation may not have added containerlab to your PATH:

```bash
# Try with full path
/usr/bin/containerlab version

# Or reinstall
bash -c "$(curl -sL https://get.containerlab.dev)"
```

### "Cannot connect to the Docker daemon"

Docker may not be running:

```bash
sudo systemctl start docker
sudo systemctl status docker
```

### "Permission denied"

Containerlab requires root privileges:

```bash
# Always use sudo with containerlab
sudo containerlab deploy -t simple-lab.clab.yml
```

### Port conflicts

If you see errors about ports in use:

```bash
# Check what's using the port
sudo lsof -i :50080

# Or use a different port for the graph
sudo containerlab graph -t simple-lab.clab.yml --port 8080
```

## Quick Reference

```bash
# Deploy a lab
sudo containerlab deploy -t <topology-file>.clab.yml

# Check lab status
sudo containerlab inspect -t <topology-file>.clab.yml

# Access a container
sudo docker exec -it clab-<lab-name>-<node-name> sh

# Visualize topology (web UI)
sudo containerlab graph -t <topology-file>.clab.yml

# Destroy a lab
sudo containerlab destroy -t <topology-file>.clab.yml

# List all running labs
sudo containerlab inspect --all
```

## System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| CPU | 2 cores | 4+ cores |
| RAM | 4 GB | 8+ GB |
| Disk | 10 GB | 20+ GB |
| OS | Linux (kernel 4.x+) | Ubuntu 22.04 LTS |

## Next Steps

Your environment is ready! Continue to [README.md](README.md) for the full lab instructions.

---

**Installation complete?** → [Start the lab](README.md)
