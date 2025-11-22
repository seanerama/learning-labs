"""Ollama Client wrapper with tool calling support"""

import ollama
import logging
import json
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class OllamaClient:
    """Wrapper for Ollama client with tool calling capabilities"""

    def __init__(self, host: str = "http://localhost:11434"):
        """
        Initialize Ollama client.

        Args:
            host: Ollama server host URL
        """
        self.host = host
        self.client = ollama.Client(host=host)

    def list_models(self) -> List[str]:
        """
        Get list of available models.

        Returns:
            List of model names
        """
        try:
            response = self.client.list()
            logger.debug(f"Raw list response: {response}")

            # Handle different response formats
            models = []
            if hasattr(response, 'models'):
                # Newer ollama library returns object with models attribute
                for model in response.models:
                    if hasattr(model, 'model'):
                        models.append(model.model)
                    elif hasattr(model, 'name'):
                        models.append(model.name)
            elif isinstance(response, dict) and 'models' in response:
                # Older format returns dict
                for model in response['models']:
                    if isinstance(model, dict):
                        models.append(model.get('name') or model.get('model', ''))
                    else:
                        models.append(str(model))

            logger.info(f"Available models: {models}")
            return models
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []

    async def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Send chat request to Ollama with optional tool support.

        Args:
            model: Model name to use
            messages: List of message dictionaries with 'role' and 'content'
            tools: Optional list of tool definitions
            stream: Whether to stream the response

        Returns:
            Response dictionary containing message and tool calls if any
        """
        try:
            logger.info(f"Sending chat request to model '{model}'")
            logger.debug(f"Messages: {messages}")

            # Build request parameters
            request_params = {
                "model": model,
                "messages": messages,
                "stream": stream
            }

            # Add tools if provided
            if tools:
                request_params["tools"] = tools
                logger.info(f"Including {len(tools)} tools in request")

            # Make the chat request
            response = self.client.chat(**request_params)

            logger.info(f"Received response from Ollama")
            logger.debug(f"Response: {response}")

            return response

        except Exception as e:
            error_msg = f"Error in chat request: {str(e)}"
            logger.error(error_msg)
            return {
                "message": {
                    "role": "assistant",
                    "content": f"Error communicating with Ollama: {str(e)}"
                }
            }

    def check_connection(self) -> bool:
        """
        Check if Ollama server is accessible.

        Returns:
            True if server is accessible, False otherwise
        """
        try:
            self.client.list()
            logger.info("Ollama connection successful")
            return True
        except Exception as e:
            logger.error(f"Ollama connection failed: {e}")
            return False

    def extract_tool_calls(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract tool calls from Ollama response.

        Args:
            response: Ollama response dictionary

        Returns:
            List of tool call dictionaries
        """
        tool_calls = []

        message = response.get("message", {})
        if "tool_calls" in message:
            tool_calls = message["tool_calls"]
            logger.info(f"Extracted {len(tool_calls)} tool calls")

        return tool_calls

    def format_tool_response(
        self,
        tool_calls: List[Dict[str, Any]],
        tool_results: List[Dict[str, Any]]
    ) -> Dict[str, str]:
        """
        Format tool results into a message for Ollama.

        Args:
            tool_calls: Original tool calls from Ollama
            tool_results: Results from executing the tools

        Returns:
            Message dictionary with tool results
        """
        # Combine tool calls with their results
        results_text = []
        for tool_call, result in zip(tool_calls, tool_results):
            tool_name = tool_call.get("function", {}).get("name", "unknown")
            result_content = result.get("result", result.get("error", "No result"))

            results_text.append(f"Tool '{tool_name}' result: {result_content}")

        return {
            "role": "tool",
            "content": "\n".join(results_text)
        }
