# MCP Lab Troubleshooting Guide

Common issues and solutions for the MCP learning lab.

## Table of Contents
- [Installation Issues](#installation-issues)
- [Ollama Issues](#ollama-issues)
- [Docker and OpenUI Issues](#docker-and-openui-issues)
- [MCP Server Issues](#mcp-server-issues)
- [Network Tools Issues](#network-tools-issues)
- [WSL-Specific Issues](#wsl-specific-issues)
- [General Debugging](#general-debugging)

---

## Installation Issues

### Docker: Permission Denied

**Symptom:**
```bash
docker: permission denied while trying to connect to the Docker daemon socket
```

**Solution:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Apply changes (or logout/login)
newgrp docker

# Verify
docker ps
```

### Python: Module Not Found

**Symptom:**
```python
ModuleNotFoundError: No module named 'fastmcp'
```

**Solution:**
```bash
# Ensure virtual environment is activated
source ~/mcp-lab/venv/bin/activate

# Verify you see (venv) in your prompt
# Install dependencies
pip install -r ~/mcp-lab/tools/requirements.txt

# Verify installation
python -c "import fastmcp; print('OK')"
```

### WSL: Command Not Found

**Symptom:**
```bash
bash: docker: command not found
```

**Solution:**
```bash
# Verify you're in WSL2
wsl --list --verbose
# Should show "VERSION 2"

# If in WSL1, upgrade to WSL2:
wsl --set-version <distro-name> 2

# Reinstall Docker in WSL
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

---

## Ollama Issues

### Ollama: Service Not Running

**Symptom:**
```bash
curl: (7) Failed to connect to localhost port 11434
```

**Solution:**
```bash
# Check if Ollama is running
ps aux | grep ollama

# If not running, start it
ollama serve &

# Or restart the service
sudo systemctl restart ollama

# Verify
curl http://localhost:11434/api/version
```

### Ollama: Model Not Found

**Symptom:**
```
Error: model 'granite4' not found
```

**Solution:**
```bash
# List installed models
ollama list

# Pull the model if missing
ollama pull granite4
# Or for smaller model:
ollama pull granite4:350m

# Verify
ollama list
```

### Ollama: Out of Memory

**Symptom:**
```
Error: failed to load model: insufficient memory
```

**Solution:**
```bash
# Use smaller model variant
ollama pull granite4:350m

# Or check available memory
free -h

# If in WSL, adjust WSL memory limit
# Edit: C:\Users\<YourUser>\.wslconfig
[wsl2]
memory=8GB

# Restart WSL
wsl --shutdown
# Then reopen WSL terminal
```

### Ollama: Model Download Stalled

**Symptom:**
Model download seems stuck at a percentage.

**Solution:**
```bash
# Cancel with Ctrl+C and retry
ollama pull granite4

# Check disk space
df -h

# If download corrupted, remove and retry
rm -rf ~/.ollama/models/blobs/*
ollama pull granite4
```

---

## Docker and OpenUI Issues

### Docker: Container Won't Start

**Symptom:**
```bash
docker ps
# Shows no openui container
```

**Solution:**
```bash
# Check container logs
docker logs openui

# Remove old container and recreate
docker rm -f openui

docker run -d \
  --name openui \
  -p 3000:8080 \
  -e OLLAMA_API_URL=http://host.docker.internal:11434 \
  -v openui-data:/app/backend/data \
  --add-host=host.docker.internal:host-gateway \
  ghcr.io/wandb/openui:latest

# Verify
docker ps | grep openui
```

### OpenUI: Can't Connect to Ollama

**Symptom:**
OpenUI shows "Failed to connect to model" or similar error.

**Solution:**
```bash
# Verify Ollama is accessible
curl http://localhost:11434/api/version

# Check Docker network can reach host
docker exec openui curl http://host.docker.internal:11434/api/version

# If fails, recreate container with correct network:
docker rm -f openui

docker run -d \
  --name openui \
  --network host \
  -e OLLAMA_API_URL=http://localhost:11434 \
  -v openui-data:/app/backend/data \
  ghcr.io/wandb/openui:latest
```

**WSL Note:** If using `--network host`, OpenUI will be on port 8080 (not 3000).

### OpenUI: Can't Access from Browser

**Symptom:**
"This site can't be reached" at http://localhost:3000

**Solution:**
```bash
# Verify container is running
docker ps | grep openui

# Check port mapping
docker port openui
# Should show: 8080/tcp -> 0.0.0.0:3000

# In WSL, verify Windows can see WSL ports
# From PowerShell:
Test-NetConnection -ComputerName localhost -Port 3000

# If blocked, add Windows Firewall rule:
New-NetFirewallRule -DisplayName "WSL OpenUI" -Direction Inbound -LocalPort 3000 -Protocol TCP -Action Allow
```

**Ubuntu Server:** Use `http://<server-ip>:3000` or SSH tunnel:
```bash
ssh -L 3000:localhost:3000 user@server
# Then access http://localhost:3000 from your local machine
```

---

## MCP Server Issues

### MCP: Config Not Found

**Symptom:**
OpenUI doesn't show MCP tools available.

**Solution:**
```bash
# Verify config file exists
cat ~/mcp-lab/tools/config.json

# Copy to OpenUI container
docker cp ~/mcp-lab/tools/config.json openui:/app/backend/.mcp/config.json

# Verify copy succeeded
docker exec openui cat /app/backend/.mcp/config.json

# Restart OpenUI
docker restart openui
```

### MCP: Tools Not Discovered

**Symptom:**
AI says it doesn't have access to network tools.

**Solution:**
```bash
# Test MCP server standalone
cd ~/mcp-lab/tools
source ~/mcp-lab/venv/bin/activate
python3 network_tools.py

# Should show available tools
# If error, check Python dependencies:
pip install -r requirements.txt

# Update config.json with correct path
# Get full path:
realpath ~/mcp-lab/tools/network_tools.py

# Edit config.json with that path
nano ~/mcp-lab/tools/config.json
```

### MCP: Import Errors

**Symptom:**
```python
ImportError: No module named 'dns'
```

**Solution:**
```bash
# Activate virtual environment
source ~/mcp-lab/venv/bin/activate

# Install all dependencies
pip install fastmcp dnspython

# Verify
python3 -c "import dns.resolver; print('OK')"
```

### MCP: Permission Denied

**Symptom:**
```bash
Permission denied: 'network_tools.py'
```

**Solution:**
```bash
# Make script executable
chmod +x ~/mcp-lab/tools/network_tools.py

# Verify shebang is correct
head -n 1 ~/mcp-lab/tools/network_tools.py
# Should show: #!/usr/bin/env python3
```

---

## Network Tools Issues

### Ping: Operation Not Permitted

**Symptom:**
```
✗ Error pinging google.com: Operation not permitted
```

**Solution:**
```bash
# Grant ping capabilities (if needed)
sudo chmod u+s /bin/ping

# Or run with specific capabilities
sudo setcap cap_net_raw+ep /bin/ping

# Test manually
ping -c 2 google.com
```

### DNS: Resolver Timeout

**Symptom:**
```
✗ DNS query timed out for example.com
```

**Solution:**
```bash
# Check DNS resolution manually
nslookup example.com

# Check /etc/resolv.conf
cat /etc/resolv.conf

# If empty or wrong, fix DNS:
# In WSL, edit /etc/wsl.conf
sudo nano /etc/wsl.conf

# Add:
[network]
generateResolvConf = false

# Create/edit /etc/resolv.conf
sudo nano /etc/resolv.conf

# Add:
nameserver 8.8.8.8
nameserver 1.1.1.1

# Restart WSL
wsl --shutdown
```

### Port Check: Connection Refused

**Symptom:**
All ports show as closed even for known-open ports.

**Solution:**
```bash
# Test manually
telnet google.com 80
# Or
nc -zv google.com 80

# Check if firewall is blocking
sudo iptables -L

# Check if running in restricted network
# Try a known-open port:
python3 -c "import socket; s=socket.socket(); s.settimeout(3); print(s.connect_ex(('google.com', 443)))"
# Should return 0 for success
```

---

## WSL-Specific Issues

### WSL: Networking Not Working

**Symptom:**
Can't reach internet from WSL, all network tools fail.

**Solution:**
```bash
# Check internet connectivity
ping 8.8.8.8

# If fails, check WSL network mode
cat /etc/wsl.conf

# Try switching network mode
# Edit C:\Users\<YourUser>\.wslconfig
[wsl2]
networkingMode=mirrored

# Or try NAT mode:
[wsl2]
networkingMode=NAT

# Restart WSL
wsl --shutdown
```

### WSL: Docker Not Starting

**Symptom:**
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

**Solution:**
```bash
# Start Docker service
sudo service docker start

# Enable Docker on startup
sudo systemctl enable docker

# Or use Docker Desktop for Windows
# (Works with WSL2 integration)
```

### WSL: Ports Not Accessible from Windows

**Symptom:**
Can't access http://localhost:3000 from Windows browser.

**Solution:**
```bash
# From WSL, find WSL IP
ip addr show eth0

# From Windows PowerShell, test port forwarding:
Test-NetConnection -ComputerName localhost -Port 3000

# If fails, manually forward port:
netsh interface portproxy add v4tov4 listenport=3000 listenaddress=0.0.0.0 connectport=3000 connectaddress=<WSL_IP>

# Or restart WSL to reset networking:
wsl --shutdown
```

---

## General Debugging

### Enable Verbose Logging

**For Ollama:**
```bash
# Stop Ollama
pkill ollama

# Start with debug logging
OLLAMA_DEBUG=1 ollama serve
```

**For Docker:**
```bash
# View live logs
docker logs -f openui

# View last 100 lines
docker logs --tail 100 openui
```

**For MCP Server:**
```python
# Add to network_tools.py at the top:
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check All Services Status

```bash
# Quick health check script
cat > ~/check-mcp-lab.sh << 'EOF'
#!/bin/bash
echo "=== MCP Lab Health Check ==="
echo ""

echo "1. Ollama Status:"
curl -s http://localhost:11434/api/version > /dev/null && echo "✓ Running" || echo "✗ Not running"

echo ""
echo "2. Docker Status:"
docker ps | grep -q openui && echo "✓ OpenUI running" || echo "✗ OpenUI not running"

echo ""
echo "3. Python Environment:"
source ~/mcp-lab/venv/bin/activate 2>/dev/null
python3 -c "import fastmcp, dns.resolver" 2>/dev/null && echo "✓ Dependencies OK" || echo "✗ Dependencies missing"

echo ""
echo "4. MCP Server:"
test -f ~/mcp-lab/tools/network_tools.py && echo "✓ Server file exists" || echo "✗ Server file missing"

echo ""
echo "5. Network Connectivity:"
ping -c 1 8.8.8.8 > /dev/null 2>&1 && echo "✓ Internet reachable" || echo "✗ No internet"

echo ""
echo "=== End Health Check ==="
EOF

chmod +x ~/check-mcp-lab.sh
~/check-mcp-lab.sh
```

### Reset Everything

If all else fails, clean slate:

```bash
# Stop and remove all containers
docker stop openui
docker rm openui
docker volume rm openui-data

# Stop Ollama
pkill ollama

# Remove virtual environment
rm -rf ~/mcp-lab/venv

# Recreate from scratch
cd ~/mcp-lab
python3 -m venv venv
source venv/bin/activate
pip install -r tools/requirements.txt

# Restart Ollama
ollama serve &

# Recreate OpenUI
docker run -d \
  --name openui \
  -p 3000:8080 \
  -e OLLAMA_API_URL=http://host.docker.internal:11434 \
  -v openui-data:/app/backend/data \
  --add-host=host.docker.internal:host-gateway \
  ghcr.io/wandb/openui:latest

# Copy config
docker cp ~/mcp-lab/tools/config.json openui:/app/backend/.mcp/config.json
docker restart openui
```

---

## Still Having Issues?

If you're still stuck:

1. **Check the health check script** output above
2. **Review logs** from Ollama and Docker
3. **Try manual testing** of each component
4. **Search for specific error messages** online
5. **Ask for help** with specific error messages and logs

### Useful Diagnostic Commands

```bash
# System info
uname -a
lsb_release -a

# Resource usage
free -h
df -h

# Network
ip addr
netstat -tuln

# Docker
docker info
docker system df

# Ollama
ollama list
ps aux | grep ollama

# Python
python3 --version
pip list | grep -E 'fastmcp|dns'
```

Include output from these commands when asking for help!
