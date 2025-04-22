import requests
import json
import os
from typing import List, Dict, Any
from orchestrator.mcp_instance import mcp
from dotenv import load_dotenv
import base64
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Spotify API configuration
SPOTIFY_API_BASE = 'https://api.spotify.com/v1'
SPOTIFY_ACCOUNTS_BASE = 'https://accounts.spotify.com'

# Load tokens from environment or file
def load_tokens() -> Dict[str, str]:
    """Load access and refresh tokens from environment or file."""
    # First try to get from environment
    access_token = os.getenv('SPOTIFY_ACCESS_TOKEN')
    refresh_token = os.getenv('SPOTIFY_REFRESH_TOKEN')
    
    if access_token and refresh_token:
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    
    # If not in environment, try to load from file
    try:
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                'servers', 'spotify-mcp-server', 'spotify-config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
            return {
                'access_token': config['accessToken'],
                'refresh_token': config['refreshToken']
            }
    except:
        raise Exception("No Spotify tokens found in environment or config file")

# Store tokens in memory
tokens = load_tokens()
token_expiry = datetime.now() + timedelta(hours=1)  # Default expiry

def refresh_access_token() -> None:
    """Refresh the access token using the refresh token."""
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        raise Exception("Spotify client credentials not found in environment")
    
    # Create basic auth header
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
    
    headers = {
        'Authorization': f'Basic {auth_base64}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': tokens['refresh_token']
    }
    
    response = requests.post(f'{SPOTIFY_ACCOUNTS_BASE}/api/token', headers=headers, data=data)
    
    if not response.ok:
        raise Exception(f"Failed to refresh token: {response.text}")
    
    response_data = response.json()
    tokens['access_token'] = response_data['access_token']
    token_expiry = datetime.now() + timedelta(seconds=response_data['expires_in'])

def make_spotify_request(method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Make an authenticated request to the Spotify API.
    
    Args:
        method: HTTP method (GET, POST, etc.)
        endpoint: API endpoint
        data: Request payload (optional)
    
    Returns:
        Response data from the API
    """
    # Check if token needs refresh
    if datetime.now() >= token_expiry:
        refresh_access_token()
    
    headers = {
        'Authorization': f'Bearer {tokens["access_token"]}',
        'Content-Type': 'application/json'
    }
    
    url = f'{SPOTIFY_API_BASE}{endpoint}'
    response = requests.request(method, url, headers=headers, json=data)
    
    if not response.ok:
        error_msg = response.json().get('error', {}).get('message', 'Unknown error')
        raise Exception(f'Spotify API error: {error_msg}')
    
    return response.json()

@mcp.tool()
def create_playlist(name: str, description: str = "", public: bool = False) -> str:
    """
    Create a new playlist on Spotify.
    
    Args:
        name: The name of the playlist
        description: Optional description of the playlist
        public: Whether the playlist should be public (default: False)
    """
    try:
        # First get the user's ID
        user_profile = make_spotify_request('GET', '/me')
        user_id = user_profile['id']
        
        # Create the playlist
        playlist = make_spotify_request('POST', f'/users/{user_id}/playlists', {
            'name': name,
            'description': description,
            'public': public
        })
        
        return playlist['id']
    except Exception as e:
        return f"Failed to create playlist: {str(e)}"

@mcp.tool()
def search_tracks(query: str, limit: int = 10) -> List[dict]:
    """
    Search for tracks on Spotify.
    
    Args:
        query: The search query (can include artist name, track name, etc.)
        limit: Maximum number of results to return (default: 10)
    
    Returns:
        List of track objects containing track name, artist, and Spotify URI
    """
    try:
        response = make_spotify_request('GET', f'/search?q={query}&type=track&limit={limit}')
        tracks = response['tracks']['items']
        
        return [{
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'uri': track['uri']
        } for track in tracks]
    except Exception as e:
        return [{'error': f"Failed to search tracks: {str(e)}"}]

@mcp.tool()
def add_tracks_to_playlist(playlist_id: str, track_uris: List[str]) -> str:
    """
    Add tracks to an existing playlist.
    
    Args:
        playlist_id: The Spotify ID of the playlist
        track_uris: List of Spotify track URIs to add to the playlist
    
    Returns:
        Success message or error message
    """
    try:
        make_spotify_request('POST', f'/playlists/{playlist_id}/tracks', {
            'uris': track_uris
        })
        return "Tracks added successfully to playlist"
    except Exception as e:
        return f"Failed to add tracks to playlist: {str(e)}"