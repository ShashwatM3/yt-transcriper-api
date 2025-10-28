from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import os
from openai import OpenAI
from dotenv import load_dotenv
from Transcripter import get_video_id, get_transcript_v2

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
    transcript = get_transcript_v2(video_id)
    return {"video_id": video_id, "transcript": transcript}