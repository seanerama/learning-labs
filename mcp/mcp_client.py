"""MCP Client using FastMCP Client for communication with MCP servers"""

import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class MCPClientWrapper:
    """Wrapper for FastMCP Client to interact with MCP servers"""

    def __init__(self, server_script: str = "mcp_server.py"):
        """
        Initialize MCP client wrapper.

        Args:
            server_script: Path to the MCP server script
        """
        self.server_script = server_script
        self._client = None
        self._tools_cache = None

    async def connect(self):
        """Connect to the MCP server"""
        from fastmcp import Client

        # FastMCP Client connects to server via subprocess
        script_path = Path(__file__).parent / self.server_script
        self._client = Client(str(script_path))
        logger.info(f"Connecting to MCP server: {script_path}")

    async def list_tools(self) -> List[Dict[str, Any]]:
        """
        Get list of available tools from MCP server.

        Returns:
            List of tool definitions
        """
        if not self._client:
            await self.connect()

        try:
            async with self._client:
                tools_response = await self._client.list_tools()
                tools = []

                for tool in tools_response:
                    tool_def = {
                        "name": tool.name,
                        "description": tool.description or "",
                        "parameters": tool.inputSchema if hasattr(tool, 'inputSchema') else {}
                    }
                    tools.append(tool_def)
                    logger.info(f"Found tool: {tool.name}")

                self._tools_cache = tools
                return tools

        except Exception as e:
            logger.error(f"Error listing tools: {e}")
            return []

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a tool on the MCP server.

        Args:
            tool_name: Name of the tool to call
            arguments: Arguments to pass to the tool

        Returns:
            Tool execution result
        """
        if not self._client:
            await self.connect()

        try:
            logger.info(f"Calling tool '{tool_name}' with args: {arguments}")

            async with self._client:
                result = await self._client.call_tool(tool_name, arguments)

                # Extract text content from result
                if hasattr(result, 'content') and result.content:
                    # Result content is a list of content items
                    text_content = []
                    for item in result.content:
                        if hasattr(item, 'text'):
                            text_content.append(item.text)
                    result_text = "\n".join(text_content) if text_content else str(result)
                else:
                    result_text = str(result)

                logger.info(f"Tool '{tool_name}' result: {result_text}")
                return {
                    "status": "success",
                    "result": result_text
                }

        except Exception as e:
            error_msg = f"Error calling tool '{tool_name}': {str(e)}"
            logger.error(error_msg)
            return {
                "status": "error",
                "error": error_msg
            }

    async def check_health(self) -> bool:
        """
        Check if MCP server is accessible.

        Returns:
            True if server responds, False otherwise
        """
        try:
            if not self._client:
                await self.connect()

            async with self._client:
                await self._client.ping()
                logger.info("MCP server health check passed")
                return True

        except Exception as e:
            logger.warning(f"MCP server health check failed: {e}")
            return False

    def get_tools_for_ollama(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Convert MCP tool definitions to Ollama tool format.

        Args:
            tools: List of MCP tool definitions

        Returns:
            List of tools in Ollama format
        """
        ollama_tools = []

        for tool in tools:
            ollama_tool = {
                "type": "function",
                "function": {
                    "name": tool.get("name"),
                    "description": tool.get("description", ""),
                    "parameters": tool.get("parameters", {
                        "type": "object",
                        "properties": {},
                        "required": []
                    })
                }
            }
            ollama_tools.append(ollama_tool)

        return ollama_tools
