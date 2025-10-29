from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import os
from openai import OpenAI
from dotenv import load_dotenv
from Transcripter import get_video_id, get_transcript_v2, get_transcript, get_transcript_instagram_reel,get_transcript_instagram_reel_raw

# client = OpenAI(
#     # This is the default and can be omitted
#     api_key=os.environ.get("OPENAI_API_KEY"),
# )

app = FastAPI(title="YouTube Transcripter API")

# Allow requests from all origins (for simplicity)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the YouTube Transcription API!"}

@app.get("/transcript")
def query(url: str = Query(..., description="Input YouTube Video URL for transcription")):
    video_id = get_video_id(url)
    # transcript = get_transcript_v2(video_id)
    transcript = get_transcript(video_id)
    return {"video_id": video_id, "transcript": transcript}

@app.get("/instagram-transcript")
def query2(url: str = Query(..., description="Input Instagram Reel URL for transcription")):
    transcript = get_transcript_instagram_reel(url)
    # transcript = get_transcript_instagram_reel_raw(url)
    return {"reel_url": url, "transcript": transcript}