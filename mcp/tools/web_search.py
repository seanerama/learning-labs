"""Web search tool (mock implementation for PoC)"""

async def web_search(query: str) -> str:
    """
    Search the web for information (mock implementation).

    Args:
        query: Search query string

    Returns:
        Mock search results
    """
    # Mock implementation for PoC
    mock_results = {
        "weather": "Current weather information is available through weather APIs",
        "python": "Python is a high-level programming language known for its simplicity",
        "ai": "Artificial Intelligence is transforming various industries",
        "ollama": "Ollama is a tool for running large language models locally"
    }

    query_lower = query.lower()
    for key, value in mock_results.items():
        if key in query_lower:
            return f"Search results for '{query}': {value}"

    return f"Search results for '{query}': No specific information found (mock implementation)"
