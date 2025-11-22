"""FastMCP Server with tool implementations"""

from fastmcp import FastMCP
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("Ollama Tools Server")

@mcp.tool()
async def calculator(expression: str) -> str:
    """
    Evaluate a mathematical expression safely.

    Args:
        expression: A mathematical expression to evaluate (e.g., "2 + 2", "10 * 5")

    Returns:
        The result of the calculation as a string
    """
    try:
        logger.info(f"Calculating: {expression}")
        # Safe evaluation with limited builtins
        result = eval(expression, {"__builtins__": {}}, {
            "abs": abs, "round": round, "min": min, "max": max,
            "sum": sum, "pow": pow
        })
        logger.info(f"Result: {result}")
        return str(result)
    except Exception as e:
        error_msg = f"Error calculating '{expression}': {str(e)}"
        logger.error(error_msg)
        return error_msg

@mcp.tool()
async def get_weather(location: str) -> str:
    """
    Get current weather for a location (mock implementation for PoC).

    Args:
        location: City name or location to get weather for

    Returns:
        Weather information as a string
    """
    logger.info(f"Getting weather for: {location}")

    # Mock weather data for PoC
    weather_data = {
        "Seattle": "52°F, Partly Cloudy",
        "New York": "45°F, Clear",
        "London": "10°C, Rainy",
        "San Francisco": "58°F, Foggy",
        "Tokyo": "18°C, Sunny",
        "Paris": "12°C, Overcast",
        "Sydney": "22°C, Sunny"
    }

    result = weather_data.get(location, f"Weather data not available for {location}")
    logger.info(f"Weather result: {result}")
    return result

@mcp.tool()
async def web_search(query: str) -> str:
    """
    Search the web for information (mock implementation for PoC).

    Args:
        query: Search query string

    Returns:
        Search results as a string
    """
    logger.info(f"Searching for: {query}")

    # Mock search results for PoC
    mock_results = {
        "weather": "Current weather varies by location. Use weather APIs for real-time data.",
        "python": "Python is a high-level, interpreted programming language known for its simplicity and readability.",
        "ai": "Artificial Intelligence (AI) is transforming industries including healthcare, finance, and technology.",
        "ollama": "Ollama is a tool for running large language models locally on your machine.",
        "fastmcp": "FastMCP is a framework for building Model Context Protocol servers.",
        "machine learning": "Machine learning is a subset of AI focused on algorithms that learn from data."
    }

    query_lower = query.lower()
    for key, value in mock_results.items():
        if key in query_lower:
            result = f"Search results for '{query}': {value}"
            logger.info(f"Search result: {result}")
            return result

    result = f"Search results for '{query}': No specific information found in mock database. Try a different query."
    logger.info(f"Search result: {result}")
    return result

if __name__ == "__main__":
    import os

    port = int(os.getenv("MCP_SERVER_PORT", "8000"))
    logger.info(f"Starting MCP server on port {port}")
    logger.info(f"Available tools: calculator, get_weather, web_search")

    # FastMCP uses its own run method
    mcp.run()
