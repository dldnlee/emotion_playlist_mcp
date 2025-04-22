from orchestrator.mcp_instance import mcp
import os
import requests

@mcp.tool()
def search_brave(refined_emotion: str) -> str:
    """
    Query Brave search MCP server with refined emotion.
    """
    response = requests.post("http://localhost:3000/tool/search", json={
        "query": refined_emotion
    }, headers={
        "Authorization": f"Bearer {os.getenv('BRAVE_API_KEY')}"
    })

    if response.ok:
        data = response.json()
        return data.get("summary", "No result found")
    else:
        return "Brave search failed"