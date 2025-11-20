# MCP Lab Quick Start

Get up and running in 15 minutes.

## Prerequisites
- Windows 11 with WSL2 (or Ubuntu Server)
- Basic command line knowledge

## Quick Setup

### 1. Install Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Pull Model
```bash
# For 8GB+ RAM systems:
ollama pull granite4

# For 4-8GB RAM systems:
ollama pull granite4:350m
```

### 3. Setup Python Environment
```bash
# Create project directory
mkdir -p ~/mcp-lab/tools
cd ~/mcp-lab

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install fastmcp dnspython
```

### 4. Run OpenUI
```bash
docker run -d \
  --name openui \
  -p 3000:8080 \
  -e OLLAMA_API_URL=http://host.docker.internal:11434 \
  -v openui-data:/app/backend/data \
  --add-host=host.docker.internal:host-gateway \
  ghcr.io/wandb/openui:latest
```

### 5. Get Lab Files
```bash
# Copy the network_tools.py from the lab
cp /home/smahoney/autocon4/kube/learning-labs/mcp/tools/* ~/mcp-lab/tools/

# Update config.json with your username
cd ~/mcp-lab/tools
sed -i "s/YOUR_USERNAME/$(whoami)/g" config.json
```

### 6. Test MCP Server
```bash
cd ~/mcp-lab/tools
source ~/mcp-lab/venv/bin/activate
python3 network_tools.py
# Should show 3 available tools
```

### 7. Connect OpenUI to MCP
```bash
# Copy config to OpenUI
docker cp ~/mcp-lab/tools/config.json openui:/app/backend/.mcp/config.json

# Restart OpenUI
docker restart openui
```

### 8. Try It Out!
1. Open http://localhost:3000
2. Select your Ollama model (granite4 or granite4:350m)
3. Ask: "Can you ping google.com and check if port 443 is open?"

## Verify Setup
```bash
# Check Ollama
curl http://localhost:11434/api/version

# Check Docker
docker ps | grep openui

# Check Python
source ~/mcp-lab/venv/bin/activate
python -c "import fastmcp; print('OK')"
```

## Troubleshooting
If something doesn't work, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## Next Steps
1. Read the [full README.md](README.md) for concepts
2. Try [Network Troubleshooting scenario](scenarios/network-troubleshooting.md)
3. Work through [challenges](scenarios/challenges.md)

## Quick Commands Reference

**Activate Python environment:**
```bash
source ~/mcp-lab/venv/bin/activate
```

**Start Ollama (if not running):**
```bash
ollama serve &
```

**Restart OpenUI:**
```bash
docker restart openui
```

**Test MCP server:**
```bash
cd ~/mcp-lab/tools
python3 network_tools.py
```

**View OpenUI logs:**
```bash
docker logs -f openui
```

---

**Ready to learn?** Continue to the [main lab](README.md) for full concepts and setup explanations!
