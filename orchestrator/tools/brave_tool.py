import os
import requests
from typing import List
from orchestrator.mcp_instance import mcp

@mcp.tool()
def search_brave(refined_emotion: str) -> List[str]:
    """
    Query Brave Search API with refined emotion and extract song titles.
    """
    api_key = os.getenv('BRAVE_API_KEY')
    if not api_key:
        return ["Brave API key not found."]

    headers = {
        'Accept': 'application/json',
        'X-Subscription-Token': api_key
    }

    params = {
        'q': refined_emotion,
        'count': 10  # Number of search results to retrieve
    }

    try:
        response = requests.get('https://api.search.brave.com/res/v1/web/search', headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract titles from the search results
        results = data.get('web', {}).get('results', [])
        if not results:
            return ["No results found."]

        # Return a list of titles as potential song names
        song_titles = [item['title'] for item in results]
        return song_titles

    except requests.exceptions.RequestException as e:
        return [f"Brave search failed: {e}"]