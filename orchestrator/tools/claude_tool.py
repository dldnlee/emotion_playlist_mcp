from orchestrator.mcp_instance import mcp
@mcp.tool()
def process_emotion(emotion: str) -> str:
    """
    Refine emotion using Claude (simulate for now).
    """
    return f"Refined version of {emotion}"