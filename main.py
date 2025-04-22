import orchestrator.tools.claude_tool
import orchestrator.tools.brave_tool
import orchestrator.tools.spotify_tool
import orchestrator.tools.get_emotion
from orchestrator.utils.env_loader import load_env
from orchestrator.mcp_instance import mcp
load_env()

if __name__ == "__main__":
    mcp.run(transport="stdio")
