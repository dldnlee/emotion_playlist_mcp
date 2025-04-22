

# Emotion Playlist MCP

## 🎯 Project Overview

Emotion Playlist MCP is an MCP-based tool that generates Spotify playlists based on the user's emotional state. It uses the Brave Search MCP Server to find songs related to a refined emotional query, and integrates with the Spotify MCP Server to create and populate playlists.

---

## 🛠 Features

- Accepts natural language input about your mood.
- Refines the emotion into a detailed search phrase.
- Searches Brave for song ideas based on the refined emotion.
- Creates Spotify playlists automatically using those ideas.

---

## 🚀 Getting Started

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/emotion_playlist_mcp.git
cd emotion_playlist_mcp
```

### 2. Setup Environment

Using `uv`:
```bash
uv init
```

Or manually:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the project root:

```
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback  # Should be identical to Spotify Developer App's redirect URI
BRAVE_API_KEY=your_brave_api_key
```
Spotify Tokens can be found in Spotify Developer

Required:
- Spotify Premium Account

---

## 🖥 Generating Auth Tokens for Spotify

```bash
python3 orchestrator/tools/spotify_auth.py
```

---

## 🖥 Running the Orchestrator

```bash
python orchestrator/main.py
```

## 🤝 Contributing

Feel free to fork, modify, and submit pull requests. Let's make mood-based music smarter together!

---

## 📄 License

MIT License
