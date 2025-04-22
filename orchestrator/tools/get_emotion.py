from mcp_instance import mcp

@mcp.tool()
def get_emotion() -> str:
    """
    Simulate or prompt for user's current emotion.
    """
    return input("Enter your emotion: ")