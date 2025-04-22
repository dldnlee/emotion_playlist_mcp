from mcp.tools import tool
import requests

@tool()
def create_playlist(refined_emotion: str, search_result: str) -> str:
    """
    Call Spotify MCP Server to create a playlist based on emotion + context.
    """
    # Example: forward to Spotify MCP (adjust for actual tool names if needed)
    payload = {
        "name": f"{refined_emotion} - {search_result[:20]}",
        "description": f"Auto-generated playlist for {refined_emotion}",
        "query": refined_emotion
    }
    response = requests.post("http://localhost:3001/tool/createPlaylistWithSearch", json=payload)

    if response.ok:
        data = response.json()
        return data.get("playlistUrl", "No playlist URL returned")
    else:
        return "Failed to create playlist"