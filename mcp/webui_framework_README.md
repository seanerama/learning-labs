# Ollama + FastMCP Chat Interface

A web-based chat interface that connects local Ollama models with FastMCP servers, enabling LLM tool-calling capabilities through an intuitive Streamlit UI.

## Architecture Overview

```mermaid
flowchart TB
    subgraph UI["Streamlit Web UI"]
        A[User Input]
        B[Chat Display]
        C[Sidebar Config]
    end

    subgraph Core["Application Core"]
        D[app.py]
        E[ollama_client.py]
        F[mcp_client.py]
    end

    subgraph External["External Services"]
        G[Ollama Server]
        H[FastMCP Server]
    end

    A --> D
    D --> B
    C --> D
    D <--> E
    D <--> F
    E <--> G
    F <--> H
```

## Request Flow

```mermaid
sequenceDiagram
    participant U as User
    participant App as Streamlit App
    participant OC as Ollama Client
    participant MC as MCP Client
    participant O as Ollama Server
    participant MCP as FastMCP Server

    U->>App: Send message
    App->>MC: Get available tools
    MC->>MCP: list_tools()
    MCP-->>MC: Tool definitions
    MC-->>App: Tools for Ollama format

    App->>OC: Chat request + tools
    OC->>O: POST /api/chat
    O-->>OC: Response (may include tool_calls)

    alt Tool calls present
        OC-->>App: Tool calls detected
        loop For each tool call
            App->>MC: call_tool(name, args)
            MC->>MCP: Execute tool
            MCP-->>MC: Tool result
            MC-->>App: Result
        end
        App->>OC: Second chat with tool results
        OC->>O: POST /api/chat
        O-->>OC: Final response
    end

    OC-->>App: Assistant response
    App->>U: Display response
```

## Component Interaction

```mermaid
flowchart LR
    subgraph Config
        Y[config.yaml]
    end

    subgraph Client["Chat Application"]
        A[app.py] --> B[ollama_client.py]
        A --> C[mcp_client.py]
    end

    subgraph Servers["MCP Servers"]
        D[example_FastMCP.py]
        E[Your Custom Server]
    end

    Y --> A
    B <--> F[Ollama API]
    C <--> D
    C <--> E
```

## Features

- Chat with local Ollama models through a clean web interface
- Tool calling support via FastMCP servers
- Multiple MCP server support with easy switching
- Persistent chat history during session
- Model selection and temperature control
- Real-time connection status monitoring
- Clean, responsive Streamlit UI

## Prerequisites

- Python 3.10 or higher
- Ollama installed and running ([Install Ollama](https://ollama.com/download))
- At least one Ollama model with tool support (e.g., `granite4:350m`, `llama3.2`, `mistral`)

## Quick Start

### 1. Install Ollama and Pull a Model

```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
ollama serve

# In another terminal, pull a model with tool support
ollama pull granite4:350m
```

### 2. Clone and Setup Project

```bash
# Clone the repository
git clone <repo-url>
cd Simple_MCPUI

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run app.py
```

The MCP server is started automatically via subprocess when needed - no separate terminal required.

### 4. Access the Application

Open your browser and navigate to: `http://localhost:8501`

## Project Structure

```
Simple_MCPUI/
├── app.py                 # Main Streamlit application
├── ollama_client.py       # Ollama API wrapper with tool support
├── mcp_client.py          # FastMCP client integration
├── example_FastMCP.py     # Example FastMCP server with sample tools
├── config.yaml            # Configuration for models and servers
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project metadata and build config
└── .env.example           # Environment variables template
```

## Configuration

### config.yaml

```yaml
ollama:
  host: "http://localhost:11434"
  models:
    - granite4:350m
    - llama3.2:1b

mcp:
  servers:
    - name: "Demo Tools"
      script: "example_FastMCP.py"
      description: "Calculator, weather, and web search tools"
  default_server: "Demo Tools"
  timeout: 30

chat:
  default_model: "granite4:350m"
  max_tokens: 2048
  temperature: 0.7
```

## Adding Custom MCP Servers

This application supports multiple FastMCP servers that can be switched via the UI. Follow these steps to add your own:

### Step 1: Create Your MCP Server

Create a new Python file with your tools using FastMCP:

```python
# my_custom_tools.py
from fastmcp import FastMCP

mcp = FastMCP("My Custom Tools")

@mcp.tool()
async def my_tool(param1: str, param2: int = 10) -> str:
    """
    Description of what the tool does.

    Args:
        param1: Description of param1
        param2: Description of param2 (default: 10)

    Returns:
        Description of return value
    """
    # Your implementation here
    result = f"Processed {param1} with value {param2}"
    return result

@mcp.tool()
async def another_tool(query: str) -> str:
    """Search for something."""
    # Implementation
    return f"Results for: {query}"

if __name__ == "__main__":
    mcp.run()
```

### Step 2: Register in config.yaml

Add your server to the `mcp.servers` list:

```yaml
mcp:
  servers:
    - name: "Demo Tools"
      script: "example_FastMCP.py"
      description: "Calculator, weather, and web search tools"

    - name: "My Custom Tools"
      script: "my_custom_tools.py"
      description: "Description of your custom tools"

    # External servers (absolute paths)
    - name: "External API Tools"
      script: "/path/to/external/api_tools.py"
      description: "External API integrations"

  default_server: "Demo Tools"
```

### Step 3: Restart the Application

```bash
# If running, stop with Ctrl+C then restart
streamlit run app.py
```

Your new server will appear in the MCP Server dropdown in the sidebar.

### MCP Server Architecture

```mermaid
flowchart TB
    subgraph App["Streamlit Application"]
        MC[mcp_client.py]
    end

    subgraph Servers["Available MCP Servers"]
        S1[example_FastMCP.py]
        S2[my_custom_tools.py]
        S3[external_server.py]
    end

    subgraph Tools1["Demo Tools"]
        T1[calculator]
        T2[get_weather]
        T3[web_search]
    end

    subgraph Tools2["Custom Tools"]
        T4[my_tool]
        T5[another_tool]
    end

    MC -->|"subprocess"| S1
    MC -->|"subprocess"| S2
    MC -->|"subprocess"| S3

    S1 --> Tools1
    S2 --> Tools2
```

### Tool Definition Best Practices

1. **Clear Descriptions**: Write detailed docstrings - the LLM uses these to decide when to call your tool
2. **Type Hints**: Always include type hints for parameters and return values
3. **Default Values**: Provide sensible defaults where appropriate
4. **Error Handling**: Return informative error messages instead of raising exceptions
5. **Async Functions**: Use `async def` for tools that perform I/O operations

```python
@mcp.tool()
async def well_documented_tool(
    required_param: str,
    optional_param: int = 100,
    flag: bool = False
) -> str:
    """
    A well-documented tool that does something useful.

    This tool demonstrates best practices for MCP tool definitions.
    The LLM will read this description to understand when to use this tool.

    Args:
        required_param: A required string parameter (e.g., "example value")
        optional_param: An optional integer with default 100
        flag: Enable special processing mode

    Returns:
        A formatted string with the processing results

    Examples:
        - "Process data X" -> calls with required_param="X"
        - "Process Y with limit 50" -> calls with required_param="Y", optional_param=50
    """
    try:
        # Implementation
        result = f"Processed: {required_param}"
        if flag:
            result += " (special mode)"
        return result
    except Exception as e:
        return f"Error processing request: {str(e)}"
```

## Usage Examples

### Basic Chat

```
User: Tell me about artificial intelligence
Assistant: [Responds with information about AI]
```

### With Tool Calling

```
User: What's 25% of 840?
Assistant: [Uses calculator tool]
25% of 840 is 210.
```

### Multiple Tools

```
User: What's the weather in Seattle and calculate 123 * 456
Assistant: [Uses get_weather and calculator tools]
The weather in Seattle is 52°F, Partly Cloudy.
123 * 456 = 56,088
```

## Troubleshooting

### Ollama not responding

- Ensure Ollama service is running: `ollama serve`
- Check accessibility: `curl http://localhost:11434/api/tags`
- Verify models are available: `ollama list`

### No models available

- Pull a model: `ollama pull granite4:350m`
- Update `config.yaml` with your model name

### MCP Server issues

- Check the sidebar "Status" section shows FastMCP as available
- Verify your server script has no syntax errors: `python my_server.py`
- Check server logs in the terminal for error messages

### Tools not appearing

- Ensure tools have the `@mcp.tool()` decorator
- Verify docstrings are present (required for tool descriptions)
- Restart the Streamlit app after adding new tools

### Port conflicts

- Streamlit default: 8501 (change with `--server.port`)
- Ollama default: 11434

## Development

### Running with Different Models

```bash
# Pull additional models
ollama pull llama3.2:1b
ollama pull mistral

# Update config.yaml models list, then restart
```

### Custom Streamlit Port

```bash
streamlit run app.py --server.port 8502
```

### Testing Your MCP Server

```bash
# Test server directly
python my_custom_tools.py

# Or use fastmcp CLI if available
fastmcp dev my_custom_tools.py
```

## Limitations

- Single user session (no multi-user support)
- No persistent chat history (resets on refresh)
- Mock implementations for weather and web search in example server
- Requires models with tool-calling support

## Resources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## License

MIT License
