"""Streamlit Chat Interface for Ollama + FastMCP"""

import streamlit as st
import asyncio
import yaml
import logging
from pathlib import Path
from typing import Dict, List, Any

from ollama_client import OllamaClient
from mcp_client import MCPClientWrapper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load configuration
@st.cache_resource
def load_config() -> Dict[str, Any]:
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

config = load_config()

# Page configuration
st.set_page_config(
    page_title="Ollama + FastMCP Chat",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Ollama + FastMCP Chat")
st.caption("Chat with local LLMs enhanced with MCP tool-calling capabilities")

# Initialize Ollama client
@st.cache_resource
def init_ollama():
    """Initialize Ollama client"""
    return OllamaClient(host=config['ollama']['host'])

def get_mcp_client(server_script: str):
    """Get MCP client instance for specified server"""
    return MCPClientWrapper(server_script=server_script)

try:
    ollama_client = init_ollama()
except Exception as e:
    st.error(f"Error initializing Ollama client: {e}")
    st.stop()

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    # Model selection
    available_models = ollama_client.list_models()
    if not available_models:
        st.warning("⚠️ No models found. Please pull a model using Ollama.")
        st.code("ollama pull granite4:350m")
        st.stop()

    default_model = config['chat']['default_model']
    if default_model not in available_models and available_models:
        default_model = available_models[0]

    selected_model = st.selectbox(
        "Model",
        options=available_models,
        index=available_models.index(default_model) if default_model in available_models else 0
    )

    # Temperature slider
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=config['chat']['temperature'],
        step=0.1
    )

    st.divider()
    st.subheader("🔧 MCP Tools")

    # Tools toggle
    use_tools = st.checkbox("Enable MCP Tools", value=True)

    # MCP Server selection
    mcp_servers = config.get('mcp', {}).get('servers', [])
    selected_server_script = None

    if use_tools and mcp_servers:
        server_names = [s['name'] for s in mcp_servers]
        default_server = config.get('mcp', {}).get('default_server', server_names[0] if server_names else None)

        selected_server_name = st.selectbox(
            "MCP Server",
            options=server_names,
            index=server_names.index(default_server) if default_server in server_names else 0,
            help="Select which MCP server to use for tools"
        )

        # Get the script path for selected server
        selected_server = next((s for s in mcp_servers if s['name'] == selected_server_name), None)
        if selected_server:
            selected_server_script = selected_server['script']
            st.caption(f"_{selected_server.get('description', '')}_")

    # Connection status
    st.divider()
    st.subheader("🔌 Status")

    ollama_status = ollama_client.check_connection()
    st.write(f"Ollama: {'🟢 Connected' if ollama_status else '🔴 Disconnected'}")

    # Check MCP status
    mcp_status = False
    if use_tools and selected_server_script:
        async def check_mcp():
            mcp = get_mcp_client(selected_server_script)
            return await mcp.check_health()

        try:
            mcp_status = asyncio.run(check_mcp())
            st.write(f"FastMCP: {'🟢 Available' if mcp_status else '🔴 Unavailable'}")
        except Exception as e:
            st.write("FastMCP: 🔴 Error")
            logger.error(f"MCP check error: {e}")
    elif use_tools:
        st.write("FastMCP: ⚠️ No servers configured")
    else:
        st.write("FastMCP: ⚪ Disabled")

    # Show available tools
    if use_tools and mcp_status and selected_server_script:
        async def get_tools():
            mcp = get_mcp_client(selected_server_script)
            return await mcp.list_tools()

        try:
            tools_list = asyncio.run(get_tools())
            if tools_list:
                with st.expander(f"Available Tools ({len(tools_list)})"):
                    for tool in tools_list:
                        st.write(f"**{tool['name']}**")
                        st.caption(tool.get('description', 'No description'))
        except Exception as e:
            logger.error(f"Error getting tools: {e}")

    # Clear chat button
    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Display tool calls if present
        if "tool_calls" in message and message["tool_calls"]:
            with st.expander("🔧 Tool Calls"):
                for tc in message["tool_calls"]:
                    st.json(tc)

# Chat processing function
async def process_chat(user_message: str, use_mcp_tools: bool, server_script: str) -> str:
    """
    Process chat message with Ollama and FastMCP tools.

    Args:
        user_message: User's input message
        use_mcp_tools: Whether to use MCP tools
        server_script: Path to MCP server script

    Returns:
        Assistant's response
    """
    try:
        # Prepare messages for Ollama
        messages = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in st.session_state.messages
        ]
        messages.append({"role": "user", "content": user_message})

        # Get tools from MCP server if enabled
        tools = None
        mcp_client = None

        if use_mcp_tools and server_script:
            mcp_client = get_mcp_client(server_script)
            mcp_tools = await mcp_client.list_tools()
            if mcp_tools:
                tools = mcp_client.get_tools_for_ollama(mcp_tools)
                logger.info(f"Loaded {len(tools)} tools from FastMCP server: {server_script}")

        # First Ollama call
        response = await ollama_client.chat(
            model=selected_model,
            messages=messages,
            tools=tools
        )

        # Check for tool calls
        tool_calls = ollama_client.extract_tool_calls(response)

        if tool_calls and mcp_client:
            logger.info(f"Processing {len(tool_calls)} tool calls via FastMCP")

            # Execute tool calls through MCP server
            tool_results = []
            for tool_call in tool_calls:
                function = tool_call.get("function", {})
                tool_name = function.get("name")
                tool_args = function.get("arguments", {})

                logger.info(f"Calling MCP tool: {tool_name} with args: {tool_args}")
                result = await mcp_client.call_tool(tool_name, tool_args)
                tool_results.append({
                    "name": tool_name,
                    "result": result.get("result", result.get("error", "No result"))
                })
                logger.info(f"MCP tool result: {result}")

            # Add assistant message with tool calls
            assistant_content = response["message"].get("content", "")
            messages.append({
                "role": "assistant",
                "content": assistant_content,
                "tool_calls": tool_calls
            })

            # Add tool results as tool message
            results_text = "\n".join([
                f"Tool '{r['name']}' result: {r['result']}"
                for r in tool_results
            ])
            messages.append({
                "role": "tool",
                "content": results_text
            })

            # Second Ollama call with tool results
            final_response = await ollama_client.chat(
                model=selected_model,
                messages=messages,
                tools=tools
            )

            # Store tool calls for display
            st.session_state.last_tool_calls = [
                {"tool": tc["function"]["name"], "args": tc["function"]["arguments"], "result": tr["result"]}
                for tc, tr in zip(tool_calls, tool_results)
            ]

            return final_response["message"]["content"]
        else:
            # No tool calls, return direct response
            st.session_state.last_tool_calls = []
            return response["message"]["content"]

    except Exception as e:
        error_msg = f"Error processing chat: {str(e)}"
        logger.error(error_msg)
        return f"❌ {error_msg}"

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = asyncio.run(process_chat(prompt, use_tools, selected_server_script))
            st.markdown(response)

            # Display tool calls if any
            if hasattr(st.session_state, 'last_tool_calls') and st.session_state.last_tool_calls:
                with st.expander("🔧 FastMCP Tool Calls"):
                    for tc in st.session_state.last_tool_calls:
                        st.write(f"**{tc['tool']}**({tc['args']}) → {tc['result']}")

    # Add assistant response to chat history
    assistant_message = {"role": "assistant", "content": response}
    if hasattr(st.session_state, 'last_tool_calls') and st.session_state.last_tool_calls:
        assistant_message["tool_calls"] = st.session_state.last_tool_calls

    st.session_state.messages.append(assistant_message)

# Footer
st.divider()
st.caption("💡 This app demonstrates FastMCP integration with Ollama. Try 'What's 25% of 840?' or 'What's the weather in Seattle?'")
