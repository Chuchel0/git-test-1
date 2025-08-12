import os
import requests
from dotenv import load_dotenv
from yt_dlp import YoutubeDL

# Load environment variables from .env file
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("Hugging Face API token not found. Please set HF_TOKEN in your .env file.")

HF_API_URL_TEMPLATE = "https://api-inference.huggingface.co/models/{}"


def transcribe_audio_from_url(audio_url: str, model: str = "openai/whisper-small") -> dict:
    """
    Transcribes audio from a URL using the Hugging Face Inference API.
    """
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    api_url = HF_API_URL_TEMPLATE.format(model)

    # It's better to stream the download to handle larger files without consuming too much memory
    with requests.get(audio_url, stream=True) as r:
        r.raise_for_status()
        # Stream the audio data directly to the Hugging Face API
        response = requests.post(api_url, headers=headers, data=r.iter_content())

    if response.status_code != 200:
        raise Exception(f"Hugging Face API request failed with status {response.status_code}: {response.text}")

    return response.json()


def get_audio_stream_url(youtube_url: str) -> dict:
    """
    Uses yt-dlp to get the direct URL for the best audio-only stream of a YouTube video.
    No video is downloaded.
    """
    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "skip_download": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)

    audio_url = None
    # In yt-dlp, format information is in the 'formats' key
    # We iterate through the available formats to find one with an audio codec but no video codec
    for f in info.get("formats", []):
        if f.get("acodec") != "none" and f.get("vcodec") == "none":
            audio_url = f.get("url")
            break

    # Fallback to any stream with audio if a dedicated audio stream is not found
    if not audio_url:
        for f in info.get("formats", []):
            if f.get("acodec") != "none":
                audio_url = f.get("url")
                break

    return {
        "audio_url": audio_url,
        "title": info.get("title"),
        "duration": info.get("duration"),
    }
