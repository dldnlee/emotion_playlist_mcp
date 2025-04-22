from mcp.server.fastmcp import FastMCP
from tools.get_emotion import get_emotion
from tools.claude_tool import process_emotion
from tools.brave_tool import search_brave
from tools.spotify_tool import create_playlist
from utils.env_loader import load_env

load_env()  # Make sure all required environment variables are set

mcp = FastMCP("EmotionPlaylistMCP")

# Register tools
mcp.register(get_emotion)
mcp.register(process_emotion)
mcp.register(search_brave)
mcp.register(create_playlist)

if __name__ == "__main__":
    mcp.run(transport="stdio")