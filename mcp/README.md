# MCP (Model Context Protocol) Learning Lab

A hands-on introduction to the Model Context Protocol (MCP) with practical network engineering tools and scenarios.

## Table of Contents
- [What You'll Learn](#what-youll-learn)
- [Prerequisites](#prerequisites)
- [Lab Overview](#lab-overview)
- [Understanding MCP](#understanding-mcp)
- [Understanding Ollama](#understanding-ollama)
- [MCP vs Traditional REST APIs](#mcp-vs-traditional-rest-apis)
- [Lab Setup](#lab-setup)
- [Building Your First MCP Tools](#building-your-first-mcp-tools)
- [Testing Your Tools](#testing-your-tools)
- [Next Steps](#next-steps)

## What You'll Learn

By completing this lab, you will:
- Understand what MCP is and why it matters for AI applications
- Learn how to run local LLMs using Ollama
- Build custom MCP tools using FastMCP (Python)
- Create network-focused tools (ping, DNS lookup, port checker)
- See practical advantages of MCP over traditional REST APIs

## Prerequisites

- **Linux environment** (WSL2, Ubuntu, or similar)
- **Basic command line** experience
- **Basic Python** knowledge (reading/understanding code)
- **Network engineering** background (understanding ping, DNS, ports)

## Lab Overview

This lab takes a progressive approach:

1. **Concepts & Setup** - Understand MCP and Ollama while setting up your environment
2. **First Tools** - Build simple network diagnostic tools with FastMCP
3. **Hands-on Testing** - Use your tools through the SimpleUI web interface
4. **Real-world Scenarios** - Apply your knowledge (separate labs in [scenarios/](scenarios/))
5. **Extension Challenges** - Advanced exercises (see [scenarios/](scenarios/))

---

## Understanding MCP

### What is MCP?

**Model Context Protocol (MCP)** is an open protocol created by Anthropic that standardizes how AI applications (like chatbots or agents) connect to external data sources and tools.

Think of MCP as a universal adapter that allows AI models to:
- **Access data sources** (databases, files, APIs)
- **Execute tools** (run commands, query systems, manipulate data)
- **Maintain context** across conversations

### Why MCP Matters

```mermaid
graph LR
    A[AI Model] --> B[MCP Server]
    B --> C[Your Tools]
    B --> D[Data Sources]
    B --> E[APIs]

    style A fill:#e1f5ff
    style B fill:#fff4e1
    style C fill:#e8f5e9
    style D fill:#e8f5e9
    style E fill:#e8f5e9
```

**Key Benefits:**
- **Standardization** - One protocol for all tool integrations
- **Security** - Controlled access to resources
- **Composability** - Mix and match tools from different sources
- **Discoverability** - AI models can discover available tools automatically

### MCP Architecture

```mermaid
sequenceDiagram
    participant User
    participant UI as SimpleUI
    participant Ollama as Ollama LLM
    participant MCP as MCP Server
    participant Tool as Network Tool

    User->>UI: "Check if google.com is reachable"
    UI->>MCP: Get available tools
    MCP-->>UI: [ping, dns_lookup, check_port]
    UI->>Ollama: Send message + available tools
    Ollama->>Ollama: Analyze request
    Ollama-->>UI: Request tool: ping("google.com")
    UI->>MCP: Execute ping("google.com")
    MCP->>Tool: Run ping command
    Tool-->>MCP: Result: 20ms latency
    MCP-->>UI: Return result
    UI->>Ollama: Send tool result
    Ollama-->>UI: "google.com is reachable with 20ms latency"
    UI->>User: Display response
```

**Components:**
1. **MCP Host** - The application using AI (SimpleUI in our lab)
2. **MCP Client** - Connects to and communicates with MCP servers
3. **MCP Server** - Exposes tools and resources to the AI
4. **Tools/Resources** - The actual functionality (your network tools)

---

## Understanding Ollama

### What is Ollama?

**Ollama** is a tool that makes it easy to run large language models (LLMs) locally on your machine.

**Why Use Ollama?**
- **Privacy** - Your data never leaves your machine
- **Cost** - No API fees, unlimited usage
- **Speed** - No network latency for API calls
- **Offline** - Works without internet connection
- **Control** - Choose your model, adjust parameters

**The Granite Models:**
- **granite4** - IBM's open-source LLM optimized for enterprise use
- **granite4:350m** - Smaller variant (350 million parameters) for low-resource systems
- Good balance of performance and resource usage for learning

---

## MCP vs Traditional REST APIs

### Traditional REST API Approach

```mermaid
graph TD
    A[User Request] --> B[Application Code]
    B --> C{Manual Parsing}
    C --> D[REST API Call 1]
    C --> E[REST API Call 2]
    C --> F[REST API Call 3]
    D --> G[Parse JSON Response]
    E --> H[Parse JSON Response]
    F --> I[Parse JSON Response]
    G --> J[Format for AI]
    H --> J
    I --> J
    J --> K[Send to AI Model]
    K --> L[AI Response]

    style B fill:#ffebee
    style C fill:#ffebee
    style G fill:#ffebee
    style H fill:#ffebee
    style I fill:#ffebee
    style J fill:#ffebee
```

**REST API Challenges:**
- You write code to parse user intent
- You manually decide which APIs to call
- You parse and format responses for the AI
- Each new tool requires integration code
- The AI can't discover or adapt to new tools

### MCP Approach

```mermaid
graph TD
    A[User Request] --> B[AI Model]
    B --> C{AI Decides}
    C --> D[MCP: Call Tool 1]
    C --> E[MCP: Call Tool 2]
    C --> F[MCP: Call Tool 3]
    D --> G[Automatic Execution]
    E --> G
    F --> G
    G --> B
    B --> H[AI Response]

    style B fill:#e8f5e9
    style C fill:#e8f5e9
    style G fill:#e8f5e9
```

**MCP Benefits:**
- AI understands user intent automatically
- AI discovers and calls appropriate tools
- Results automatically flow back to AI
- Adding tools is just configuration
- AI can chain multiple tools intelligently

### Practical Example

**Scenario:** User asks "Is google.com down? Check both ping and DNS"

**With REST APIs:**
```python
# You write this code
def check_website(url):
    # Parse what user wants
    if "ping" in user_request:
        result1 = requests.get(f"http://api.example.com/ping/{url}")
        ping_data = result1.json()

    if "dns" in user_request:
        result2 = requests.get(f"http://api.example.com/dns/{url}")
        dns_data = result2.json()

    # Format for AI
    formatted = f"Ping: {ping_data}, DNS: {dns_data}"

    # Send to AI
    ai_response = call_ai_model(formatted)
```

**With MCP:**
```python
# You write this once
@mcp.tool()
async def ping(hostname: str) -> str:
    """Check if a host is reachable"""
    # Implementation
    return result

@mcp.tool()
async def dns_lookup(hostname: str) -> str:
    """Resolve DNS for a hostname"""
    # Implementation
    return result

# AI handles everything else automatically
# - Understands user wants both ping and DNS
# - Calls both tools
# - Interprets results
# - Responds to user
```

### Comparison Table

| Aspect | Traditional REST | MCP |
|--------|-----------------|-----|
| **Tool Discovery** | Hardcoded in application | AI discovers automatically |
| **Intent Parsing** | Manual string parsing | AI understands naturally |
| **Orchestration** | You write logic | AI chains tools intelligently |
| **Adding Tools** | Write integration code | Define tool schema |
| **Adaptability** | Fixed workflows | AI adapts to user needs |
| **Development Time** | High (lots of glue code) | Low (define tools, AI handles rest) |
| **Maintenance** | Update every integration | Update tool definitions |

---

## Lab Setup

### Step 1: Verify Environment

**What:** Ensure you have a working Linux environment.

**Why:** Ollama and the lab tools work best in Linux. WSL2 provides full Linux kernel compatibility on Windows.

```bash
# Verify your environment
uname -a
# Should show: Linux ...

# Check Python version
python3 --version
# Should be 3.10 or higher
```

### Step 2: Install Ollama

**What:** Ollama is the runtime that executes LLMs locally.

**Why:** We need a local AI model to demonstrate MCP tool integration without relying on external APIs.

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Verify installation
ollama --version
```

**How it works:**
- Ollama runs as a background service
- Listens on `http://localhost:11434` by default
- Manages model downloads and execution
- Provides OpenAI-compatible API

### Step 3: Pull the Granite Model

**What:** Download the IBM Granite 4 language model.

**Why:** Granite4 is a capable open-source model good for learning and testing. The smaller variant works on modest hardware.

```bash
# For systems with 8GB+ RAM and decent CPU/GPU
ollama pull granite4

# For low-resource systems (4-8GB RAM)
ollama pull granite4:350m
```

**Verify the model:**
```bash
# List installed models
ollama list

# Test the model
ollama run granite4:350m

# Type a test message, then /bye to exit
```

### Step 4: Install uv (Python Package Manager)

**What:** Install uv, a fast Python package and project manager.

**Why:** uv is significantly faster than pip (10-100x) and provides better dependency resolution. It's written in Rust and designed as a drop-in replacement for pip, venv, and pip-tools.

**uv vs pip:**
| Feature | pip | uv |
|---------|-----|-----|
| Speed | Baseline | 10-100x faster |
| Dependency Resolution | Basic | Advanced (like cargo) |
| Lock Files | Requires pip-tools | Built-in |
| Virtual Environments | Separate tool (venv) | Integrated |
| Caching | Basic | Aggressive, global cache |

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

### Step 5: Clone the Lab Repository

**What:** Get the learning lab files.

**Why:** This repository contains the MCP server examples and network tools you'll be working with.

```bash
# Clone the learning labs repository
git clone https://github.com/seanerama/learning-labs.git
cd learning-labs/mcp
```

### Step 6: Clone and Set Up SimpleUI

**What:** Clone the SimpleUI web interface that connects Ollama with MCP servers.

**Why:** SimpleUI provides a web-based chat interface that lets you interact with your MCP tools through a local LLM. It handles the communication between Ollama and your MCP servers.

```bash
# Clone SimpleUI into the mcp directory
git clone https://github.com/seanerama/SimpleUI.git

# Enter the SimpleUI directory
cd SimpleUI

# Create virtual environment and install dependencies
uv venv && source .venv/bin/activate && uv pip install -r requirements.txt

# Return to the mcp directory
cd ..
```

**What gets installed:**
- `streamlit` - Web UI framework
- `fastmcp` - Framework for building MCP servers
- `ollama` - Python client for Ollama API
- Other supporting libraries

### Step 7: Install Lab Dependencies

**What:** Install additional dependencies needed for the network tools.

**Why:** The network tools MCP server requires `dnspython` for DNS lookups.

```bash
# Make sure you're in the mcp directory with venv activated
source SimpleUI/.venv/bin/activate

# Install lab-specific dependencies
uv pip install dnspython>=2.4.0
```

### Step 8: Configure SimpleUI for Lab Tools

**What:** Update SimpleUI's configuration to include the lab's MCP servers.

**Why:** SimpleUI needs to know about your network tools server to make it available in the UI.

Edit `SimpleUI/config.yaml` and add the lab's MCP servers:

```yaml
# Add these to the mcp.servers list in config.yaml
mcp:
  servers:
    - name: "Network Tools"
      script: "../network_tools.py"
      description: "Network diagnostic tools: ping, DNS lookup, port check"
    - name: "Demo Tools"
      script: "../example_FastMCP.py"
      description: "Calculator, weather, and web search tools"
```

Or replace the entire `mcp.servers` section with the above.

### Step 9: Verify Full Setup

**What:** Quick checklist to ensure everything is working.

**Why:** Better to catch issues now before diving into the lab.

```bash
# 1. Check Ollama is running
curl http://localhost:11434/api/version
# Should return version info like: {"version":"0.x.x"}

# 2. Check Python environment
python3 -c "import fastmcp; print('FastMCP ready')"
python3 -c "import streamlit; print('Streamlit ready')"

# 3. Test the network tools server directly
python3 network_tools.py
# Should show FastMCP banner - press Ctrl+C to stop
```

---

## Building Your First MCP Tools

The lab includes a pre-built `network_tools.py` file with three network diagnostic tools. Let's understand how it works.

### Understanding the Network Tools Server

Open `network_tools.py` and examine its structure:

```python
from fastmcp import FastMCP

# Initialize MCP server with a name
mcp = FastMCP("Network Tools")

@mcp.tool()
async def ping(hostname: str, count: int = 4) -> str:
    """
    Check if a host is reachable using ICMP ping.

    Args:
        hostname: The hostname or IP address to ping
        count: Number of ping packets to send (default: 4)

    Returns:
        Ping results including latency and packet loss
    """
    # Implementation here...
```

**Key Concepts:**

1. **FastMCP Initialization:**
   ```python
   mcp = FastMCP("Network Tools")
   ```
   - Creates an MCP server named "Network Tools"
   - This name appears when tools are discovered

2. **Tool Decorator:**
   ```python
   @mcp.tool()
   async def ping(hostname: str, count: int = 4) -> str:
   ```
   - `@mcp.tool()` registers the function as an MCP tool
   - Type hints help the AI understand parameters
   - Async functions allow non-blocking I/O operations

3. **Docstrings are Critical:**
   - The AI reads docstrings to understand what the tool does
   - Clear descriptions help the AI decide when to use each tool
   - Document all parameters and return values

### The Three Network Tools

| Tool | Purpose | Example Usage |
|------|---------|---------------|
| `ping` | Check host reachability | "Is google.com reachable?" |
| `dns_lookup` | Resolve DNS records | "What's the IP for github.com?" |
| `check_port` | Test TCP port status | "Is port 443 open on google.com?" |

### Adding Your Own Tool

To add a new tool, follow this pattern:

```python
@mcp.tool()
async def my_new_tool(required_param: str, optional_param: int = 10) -> str:
    """
    Brief description of what this tool does.

    Args:
        required_param: Description of this parameter
        optional_param: Description with default value noted

    Returns:
        Description of what gets returned
    """
    try:
        # Your implementation
        result = f"Processed {required_param}"
        return result
    except Exception as e:
        return f"Error: {str(e)}"
```

---

## Testing Your Tools

### Start the Web Interface

```bash
# Make sure you're in the mcp directory with venv activated
cd learning-labs/mcp
source SimpleUI/.venv/bin/activate

# Start the Streamlit app
streamlit run SimpleUI/app.py
```

Open your browser to: **http://localhost:8501**

### Understanding the Interface

The SimpleUI interface has:

1. **Sidebar (left)**
   - Model selection (granite4:350m)
   - MCP Server selection (Network Tools, Demo Tools)
   - Temperature slider
   - Connection status indicators

2. **Chat Area (center)**
   - Message input at bottom
   - Conversation history above
   - Tool calls shown inline

### Try Your Network Tools

Let's test the tools and observe what happens behind the scenes.

**Step 1:** In the SimpleUI chat, type:
```
What is the latency to google.com?
```

**Step 2:** After you see the response, switch back to the terminal where Streamlit is running. You'll see detailed logs showing exactly what happened:

```
INFO     Starting MCP server 'Network Tools' with transport 'stdio'
INFO     Processing request of type ListToolsRequest
INFO     Found tool: ping
INFO     Found tool: dns_lookup
INFO     Found tool: check_port
INFO     Loaded 3 tools from FastMCP server: ../network_tools.py
INFO     Sending chat request to model 'granite4:350m'
INFO     Including 3 tools in request
INFO     HTTP Request: POST http://localhost:11434/api/chat "HTTP/1.1 200 OK"
INFO     Received response from Ollama
INFO     Extracted 2 tool calls
INFO     Processing 2 tool calls via FastMCP
INFO     Calling MCP tool: ping with args: {'count': 4, 'hostname': 'google.com'}
INFO     Pinging google.com with 4 packets
INFO     Ping successful: google.com
INFO     Tool 'ping' result: ✓ google.com is reachable...
INFO     Calling MCP tool: check_port with args: {'hostname': 'google.com', 'port': 80}
INFO     Checking port 80 on google.com
INFO     ✓ Port 80 is OPEN on google.com (service: http)
INFO     Sending chat request to model 'granite4:350m'
INFO     Received response from Ollama
```

### Understanding the Log Output

The logs reveal the complete MCP workflow:

| Log Message | What's Happening |
|-------------|------------------|
| `Starting MCP server` | SimpleUI launches your network_tools.py as an MCP server |
| `Processing request of type ListToolsRequest` | SimpleUI asks "what tools do you have?" |
| `Found tool: ping, dns_lookup, check_port` | MCP server reports its available tools |
| `Sending chat request to model` | Your question + tool definitions sent to Ollama |
| `Extracted 2 tool calls` | Ollama decided to call ping AND check_port |
| `Calling MCP tool: ping` | SimpleUI executes the ping tool via MCP |
| `Tool 'ping' result: ✓ google.com is reachable` | Tool returns results |
| `Sending chat request to model` (second time) | Results sent back to Ollama for interpretation |

**Key Insight:** Notice how the AI decided on its own to call both `ping` and `check_port` - you didn't have to specify which tools to use!

### More Example Prompts

1. **DNS Lookup:**
   ```
   What are the DNS A records for github.com?
   ```

2. **Port Check:**
   ```
   Is port 443 open on google.com?
   ```

3. **Combined Diagnostics:**
   ```
   Check if microsoft.com is up by pinging it and checking if port 80 is open
   ```

4. **Network Troubleshooting:**
   ```
   I can't reach example.com. Can you help diagnose the issue?
   Check DNS resolution, ping, and common ports (80, 443)
   ```

### What to Observe

- The AI understands your natural language request
- The AI automatically chooses which tools to use
- Tool calls are shown in the chat (you can see what's being executed)
- The AI can chain multiple tools together
- The AI interprets results and explains them
- You didn't write any orchestration code!

### Switching MCP Servers

In the sidebar, you can switch between:
- **Network Tools** - Your ping, DNS, and port check tools
- **Demo Tools** - Calculator, weather (mock), and web search (mock)

Try: "What's 25% of 840?" with Demo Tools selected.

---

## How It All Works Together

```mermaid
flowchart TB
    subgraph UI["SimpleUI (Streamlit)"]
        A[User Input]
        B[Chat Display]
        C[Sidebar Config]
    end

    subgraph Core["SimpleUI Core"]
        D[app.py]
        E[ollama_client.py]
        F[mcp_client.py]
    end

    subgraph Servers["Lab MCP Servers"]
        G[network_tools.py]
        H[example_FastMCP.py]
    end

    subgraph External["External Services"]
        I[Ollama LLM]
    end

    A --> D
    D --> B
    C --> D
    D <--> E
    D <--> F
    E <--> I
    F <--> G
    F <--> H
```

**Request Flow:**
1. User types a message in the UI
2. App.py gets available tools from the selected MCP server
3. Message + tools are sent to Ollama
4. Ollama decides if/which tools to call
5. Tool calls are executed via the MCP server
6. Results are sent back to Ollama
7. Ollama generates final response
8. Response is displayed to user

---

## Next Steps

Congratulations! You've successfully:
- Set up a local LLM environment with Ollama
- Created MCP tools using FastMCP
- Integrated tools with an AI interface
- Seen the power of MCP vs traditional approaches

### Continue Learning

1. **Add More Tools** - Extend `network_tools.py` with:
   - Traceroute
   - Whois lookup
   - HTTP status checker
   - SSL certificate checker

2. **Create a New MCP Server** - Build tools for:
   - Log file analysis
   - Configuration validation
   - System health monitoring

3. **Explore Scenarios** - Check the [scenarios/](scenarios/) directory for:
   - Network Troubleshooting Lab
   - Log Analysis Lab
   - Automated Documentation Lab

### Project Structure Reference

```
learning-labs/mcp/
├── SimpleUI/              # Cloned SimpleUI repository
│   ├── app.py             # Main Streamlit application
│   ├── ollama_client.py   # Ollama API wrapper with tool support
│   ├── mcp_client.py      # FastMCP client integration
│   ├── config.yaml        # Configuration for models and servers
│   └── requirements.txt   # Python dependencies
├── network_tools.py       # Network diagnostic MCP server (lab file)
├── example_FastMCP.py     # Demo tools MCP server (lab file)
└── README.md              # This file
```

### Additional Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- [Ollama Documentation](https://ollama.ai/docs)
- [Streamlit Documentation](https://docs.streamlit.io)
- [SimpleUI Repository](https://github.com/seanerama/SimpleUI)

---

## Troubleshooting

### Ollama not responding

```bash
# Check if Ollama is running
curl http://localhost:11434/api/version

# Start Ollama if needed
ollama serve
```

### No models available

```bash
# List available models
ollama list

# Pull a model if needed
ollama pull granite4:350m
```

### MCP Server issues

```bash
# Test the server directly
python3 network_tools.py
# Should show FastMCP banner

# Check for import errors
python3 -c "import dns.resolver; print('dnspython OK')"
```

### Tools not appearing in UI

1. Ensure the correct MCP Server is selected in the sidebar
2. Check that `SimpleUI/config.yaml` has the correct paths to your MCP servers
3. Verify the script paths are relative to the SimpleUI directory (use `../network_tools.py`)
4. Restart the Streamlit app after config changes

### Port conflicts

- Streamlit default: 8501 (change with `--server.port`)
- Ollama default: 11434

---

**Happy Learning!**

For questions or issues, check the troubleshooting section above or consult the additional resources.
