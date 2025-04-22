# servers/run_servers.py
import subprocess
import os

# Start Spotify MCP
subprocess.Popen(["node", "servers/spotify-mcp-server/build/index.js"])

# Start Brave MCP
subprocess.Popen(["node", "servers/brave-search-mcp-server/index.js"])

print("Servers launched.")