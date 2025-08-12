from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, HttpUrl
from . import services

# Pydantic model for the request body to ensure the URL is valid
class ProcessRequest(BaseModel):
    url: HttpUrl

app = FastAPI(
    title="SceneSage API",
    description="API for processing videos to extract knowledge.",
    version="0.1.0",
)

@app.get("/", tags=["General"])
def read_root():
    """ A simple endpoint to check if the API is running. """
    return {"message": "Welcome to the SceneSage API"}

@app.post("/process", tags=["Processing"])
async def process_video(request: ProcessRequest):
    """
    Accepts a YouTube URL, extracts the audio, and returns the transcription.

    This is the first step of the pipeline. For this prototype, it's a synchronous
    operation, but in a production environment, this would trigger a background job.
    """
    try:
        # Step 1: Get the direct audio stream URL from the YouTube link
        video_info = services.get_audio_stream_url(str(request.url))
        audio_url = video_info.get("audio_url")

        if not audio_url:
            raise HTTPException(
                status_code=404,
                detail="Could not find an audio stream for the provided YouTube URL."
            )

        # Step 2: Transcribe the audio using the Hugging Face API
        transcription_result = services.transcribe_audio_from_url(audio_url)

        # The result from Whisper is usually in a 'text' field
        transcribed_text = transcription_result.get("text", "Transcription not available.")

        return {
            "source_url": str(request.url),
            "title": video_info.get("title"),
            "duration_seconds": video_info.get("duration"),
            "transcription": transcribed_text,
        }

    except Exception as e:
        # Catch-all for errors from yt-dlp, requests, or the HF API
        # In a real app, you would have more granular error handling and logging
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
