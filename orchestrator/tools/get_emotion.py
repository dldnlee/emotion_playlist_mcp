from orchestrator.mcp_instance import mcp

@mcp.tool()
def get_emotion(emotion: str) -> str:
    """
    Accept the user's emotion from MCP client (e.g., Claude) and convert it into detailed search text.
    """
    emotion = emotion.strip().lower()
    detailed_emotions = {
        "happy": "uplifting and joyful music recommendations",
        "sad": "comforting and soothing songs for a melancholic mood",
        "calm": "relaxing and peaceful soundtracks to unwind",
        "angry": "high-energy and cathartic tracks to release tension",
        "nostalgic": "classic hits and emotional ballads that evoke memories",
        "excited": "energetic and uplifting tracks to get you pumped",
        "relaxed": "smooth and soothing melodies to unwind",
        "energetic": "upbeat and dynamic tracks to keep you moving",
        "motivated": "inspiring and uplifting songs to boost your spirits",
        "grateful": "thankful and positive tracks to express appreciation",
        "anxious": "calming and soothing tracks to reduce stress",
        "bored": "engaging and upbeat songs to liven up your day",
        "frustrated": "energetic and cathartic tracks to release tension",
        "grateful": "thankful and positive tracks to express appreciation"
    }

    return detailed_emotions.get(emotion, f"music suitable for feeling {emotion}")