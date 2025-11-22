"""Calculator tool for mathematical operations"""

async def calculator(expression: str) -> str:
    """
    Evaluate a mathematical expression safely.

    Args:
        expression: Mathematical expression to evaluate

    Returns:
        Result as string or error message
    """
    try:
        # Safe evaluation with limited builtins
        result = eval(expression, {"__builtins__": {}}, {
            "abs": abs, "round": round, "min": min, "max": max,
            "sum": sum, "pow": pow
        })
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"
