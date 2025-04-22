import requests
from mcp_instance import mcp

@mcp.tool()
def create_playlist(name: str, description: str = "", public: bool = False) -> str:
    """
    Create a new playlist on Spotify.
    
    Args:
        name: The name of the playlist
        description: Optional description of the playlist
        public: Whether the playlist should be public (default: False)
    """
    payload = {
        "name": name,
        "description": description,
        "public": public
    }
    
    # The Spotify MCP server runs on port 3001 by default
    response = requests.post("http://localhost:3001/tool/createPlaylist", json=payload)

    if response.ok:
        data = response.json()
        # The response will contain the playlist ID in the content text
        return data.get("content", [{}])[0].get("text", "Playlist created but no ID returned")
    else:
        return f"Failed to create playlist: {response.text}"