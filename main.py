from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import os
from openai import OpenAI
from dotenv import load_dotenv
from Transcripter import get_video_id, get_transcript_v2, get_transcript, get_transcript_anything ,get_transcript_instagram_reel_raw

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
def query(url: str = Query(..., description="Input YouTube Video URL / Instagram Reel for transcription")):
      transcript = get_transcript_anything(url)
      return {"vid_url": url, "transcript": transcript}