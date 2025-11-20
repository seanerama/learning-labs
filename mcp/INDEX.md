# MCP Learning Lab - Complete Index

Quick navigation to all lab resources.

## Getting Started

| Document | Description | Time | Audience |
|----------|-------------|------|----------|
| [QUICKSTART.md](QUICKSTART.md) | Get up and running fast | 15 min | Everyone - start here if you want to dive in |
| [README.md](README.md) | Complete lab with concepts & setup | 90 min | Everyone - comprehensive learning path |
| [MCP-VS-REST.md](MCP-VS-REST.md) | Visual comparison of approaches | 20 min | Developers who know REST APIs |

## Core Tools

| File | Description | Lines |
|------|-------------|-------|
| [tools/network_tools.py](tools/network_tools.py) | MCP server with 3 network tools | 140 |
| [tools/requirements.txt](tools/requirements.txt) | Python dependencies | 2 |
| [tools/config.json](tools/config.json) | MCP server configuration | 9 |

**Tools included:**
- `ping(hostname, count)` - Check host reachability
- `dns_lookup(hostname, record_type)` - DNS resolution
- `check_port(hostname, port, timeout)` - TCP port checking

## Real-World Scenarios

| Scenario | Level | Time | Focus |
|----------|-------|------|-------|
| [scenarios/network-troubleshooting.md](scenarios/network-troubleshooting.md) | Beginner | 30 min | Systematic troubleshooting workflows |
| [scenarios/log-analysis.md](scenarios/log-analysis.md) | Intermediate | 45 min | AI-powered log analysis & correlation |
| [scenarios/automated-docs.md](scenarios/automated-docs.md) | Intermediate | 45 min | Auto-generate network documentation |

## Challenges & Extensions

| Document | Description | Count |
|----------|-------------|-------|
| [scenarios/challenges.md](scenarios/challenges.md) | Coding challenges to extend your skills | 25 exercises |
| [scenarios/README.md](scenarios/README.md) | Learning paths & scenario overview | - |

**Challenge levels:**
- Beginner (5 challenges): Traceroute, batch operations, calculators
- Intermediate (5 challenges): Log stats, backups, geolocation, speed tests
- Advanced (5 challenges): SNMP, Netmiko, packet analysis, topology
- Expert (5 challenges): Event correlation, compliance, ML-based detection
- Bonus (5 challenges): NLP queries, ChatOps, digital twin

## Support

| Document | Purpose |
|----------|---------|
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Common issues and solutions |

**Covered topics:**
- Installation issues (Docker, Python, WSL)
- Ollama issues (service, models, memory)
- Docker/OpenUI issues (networking, access)
- MCP server issues (config, discovery, imports)
- Network tool issues (permissions, DNS, connectivity)
- WSL-specific issues (networking, Docker, port forwarding)
- General debugging techniques

## Learning Paths

### Path 1: Quick Start (2 hours total)
1. [QUICKSTART.md](QUICKSTART.md) - 15 min
2. [scenarios/network-troubleshooting.md](scenarios/network-troubleshooting.md) - 30 min
3. Try 3 beginner challenges from [scenarios/challenges.md](scenarios/challenges.md) - 60 min

### Path 2: Comprehensive (5+ hours)
1. [README.md](README.md) - 90 min
2. [scenarios/network-troubleshooting.md](scenarios/network-troubleshooting.md) - 30 min
3. [scenarios/log-analysis.md](scenarios/log-analysis.md) - 45 min
4. [scenarios/automated-docs.md](scenarios/automated-docs.md) - 45 min
5. Complete challenges - ongoing

### Path 3: Concepts Deep Dive (3 hours)
1. [README.md](README.md) - Concepts sections - 45 min
2. [MCP-VS-REST.md](MCP-VS-REST.md) - 20 min
3. [README.md](README.md) - Setup & Building Tools - 45 min
4. [scenarios/network-troubleshooting.md](scenarios/network-troubleshooting.md) - 30 min
5. Read all scenario introductions - 30 min

### Path 4: Security Focus (4 hours)
1. [README.md](README.md) - Setup - 60 min
2. [scenarios/log-analysis.md](scenarios/log-analysis.md) - Complete all exercises - 90 min
3. Security challenges (#11, #17, #18, #23) from [scenarios/challenges.md](scenarios/challenges.md) - 90 min

### Path 5: Automation Focus (4 hours)
1. [README.md](README.md) - Setup - 60 min
2. [scenarios/automated-docs.md](scenarios/automated-docs.md) - Complete all exercises - 60 min
3. [scenarios/log-analysis.md](scenarios/log-analysis.md) - Automation sections - 30 min
4. Automation challenges (#7, #12, #17, #22) from [scenarios/challenges.md](scenarios/challenges.md) - 90 min

## By File Size

| File | Size | Lines | Purpose |
|------|------|-------|---------|
| [README.md](README.md) | 23 KB | 1,000+ | Main lab guide |
| [scenarios/automated-docs.md](scenarios/automated-docs.md) | 16 KB | 650+ | Documentation automation |
| [MCP-VS-REST.md](MCP-VS-REST.md) | 14 KB | 550+ | Comparison deep dive |
| [scenarios/log-analysis.md](scenarios/log-analysis.md) | 14 KB | 550+ | Log analysis lab |
| [scenarios/challenges.md](scenarios/challenges.md) | 12 KB | 600+ | 25 coding challenges |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | 12 KB | 500+ | Troubleshooting guide |
| [scenarios/README.md](scenarios/README.md) | 7.9 KB | 350+ | Scenario overview |
| [scenarios/network-troubleshooting.md](scenarios/network-troubleshooting.md) | 6.8 KB | 350+ | Troubleshooting lab |
| [tools/network_tools.py](tools/network_tools.py) | 3.6 KB | 140 | MCP server code |
| [QUICKSTART.md](QUICKSTART.md) | 2.6 KB | 110+ | Quick setup guide |

**Total:** ~112 KB of documentation and code

## Key Concepts Covered

1. **MCP (Model Context Protocol)**
   - What it is and why it matters
   - Architecture and components
   - Protocol flow
   - See: [README.md](README.md) sections on "Understanding MCP"

2. **Ollama**
   - Local LLM runtime
   - Model management
   - Integration with MCP
   - See: [README.md](README.md) section on "Understanding Ollama"

3. **MCP vs REST**
   - Architectural differences
   - Code comparison
   - When to use each
   - See: [MCP-VS-REST.md](MCP-VS-REST.md)

4. **FastMCP Framework**
   - Building MCP servers in Python
   - Tool decorators
   - Type hints and schemas
   - See: [README.md](README.md) section on "Building Your First MCP Tools"

5. **Network Diagnostics**
   - Ping for connectivity
   - DNS resolution
   - Port checking
   - See: All scenario files

6. **AI-Assisted Operations**
   - Natural language queries
   - Intelligent tool selection
   - Result interpretation
   - See: All scenarios

7. **Log Analysis**
   - Pattern detection
   - Event correlation
   - Security analysis
   - See: [scenarios/log-analysis.md](scenarios/log-analysis.md)

8. **Documentation Automation**
   - Inventory generation
   - Multiple output formats
   - Topology diagrams
   - See: [scenarios/automated-docs.md](scenarios/automated-docs.md)

## Mermaid Diagrams Included

1. **MCP Architecture** - [README.md](README.md)
2. **MCP Sequence Diagram** - [README.md](README.md)
3. **Traditional REST Flow** - [README.md](README.md)
4. **MCP Flow** - [README.md](README.md)
5. **Troubleshooting Decision Tree** - [scenarios/network-troubleshooting.md](scenarios/network-troubleshooting.md)
6. **Network Topology Examples** - [scenarios/automated-docs.md](scenarios/automated-docs.md)
7. **REST Architecture** - [MCP-VS-REST.md](MCP-VS-REST.md)
8. **MCP Architecture Comparison** - [MCP-VS-REST.md](MCP-VS-REST.md)

## Prerequisites

**System Requirements:**
- Windows 11 with WSL2 or Ubuntu Server
- 4-8GB RAM (for granite4:350m) or 8GB+ (for granite4)
- Docker installed
- Python 3.8+

**Knowledge Requirements:**
- Network engineering background
- Basic command line skills
- Basic Python reading ability
- Understanding of ping, DNS, ports

## What You'll Build

By the end of this lab, you'll have:
- A working MCP server with network tools
- Integration with local LLM (Ollama)
- Web interface (OpenUI) for AI interaction
- Experience with 3+ real-world scenarios
- Skills to build custom MCP tools
- Understanding of AI-assisted network operations

## Additional Resources

- [MCP Official Documentation](https://modelcontextprotocol.io/)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- [Ollama Documentation](https://ollama.ai/docs)
- [OpenUI GitHub](https://github.com/wandb/openui)

## Quick Reference Commands

```bash
# Activate Python environment
source ~/mcp-lab/venv/bin/activate

# Start Ollama
ollama serve &

# Test MCP server
cd ~/mcp-lab/tools && python3 network_tools.py

# Restart OpenUI
docker restart openui

# View logs
docker logs -f openui

# Check Ollama
curl http://localhost:11434/api/version

# List models
ollama list
```

## Navigation

Start your journey:
- **New to MCP?** → [QUICKSTART.md](QUICKSTART.md)
- **Want full understanding?** → [README.md](README.md)
- **Know REST APIs?** → [MCP-VS-REST.md](MCP-VS-REST.md)
- **Ready to practice?** → [scenarios/README.md](scenarios/README.md)
- **Hit an issue?** → [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Total Learning Time:** 2-8 hours depending on path chosen
**Difficulty:** Beginner to Advanced
**Target Audience:** Network Engineers learning AI-assisted operations

---

*Lab created for network engineers to learn MCP, Ollama, and AI-assisted network operations.*
