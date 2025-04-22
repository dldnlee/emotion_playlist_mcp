from mcp.tools import tool

@tool()
def process_emotion(emotion: str) -> str:
    """
    Refine emotion using Claude (simulate for now).
    """
    return f"Refined version of {emotion}"