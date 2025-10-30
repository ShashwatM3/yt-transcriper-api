import requests
import re
import json
import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
from urllib.parse import urlparse, parse_qs
from supadata import Supadata

load_dotenv()
YOUTUBE_TRANSCRIPT_API_TOKEN = os.getenv("YOUTUBE_TRANSCRIPT_API_TOKEN")

supadata = Supadata(api_key=f"{os.getenv("SUPADATA_API_KEY")}")

ytt_api = YouTubeTranscriptApi(
    proxy_config=WebshareProxyConfig(
        proxy_username="nlgdkwab",
        proxy_password="nty0f4tbta29",
    )
)

def get_transcript(id):
  response = requests.post(
  "https://www.youtube-transcript.io/api/transcripts",
    headers={
      "Authorization": f"Basic {YOUTUBE_TRANSCRIPT_API_TOKEN}",
      "Content-Type": "application/json"
    },
    json={"ids": [id]}
  )

  transcript = []

  if response.status_code == 200:
      data = response.json()
      for dataItem in data:
        for i in dataItem["tracks"]:
          for transcript_segment in i["transcript"]:
              transcript.append(transcript_segment['text'])

      joined_text = " ".join(transcript)
      return [dataItem["title"], joined_text]
  else:
      return(f"Request failed with status code: {response.status_code}")

def get_video_id(url: str):
    """
    Extracts the YouTube video ID from a URL.
    Supports youtu.be, youtube.com/watch, and youtube.com/embed formats.
    Returns None if no valid ID is found.
    """
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Case 1: Short youtu.be link
    if parsed_url.netloc in ("youtu.be", "www.youtu.be"):
        return parsed_url.path.strip("/")
    
    # Case 2: Standard YouTube watch link
    if parsed_url.path == "/watch":
        query_params = parse_qs(parsed_url.query)
        return query_params.get("v", [None])[0]
    
    # Case 3: Embed or other formats
    match = re.search(r"/embed/([a-zA-Z0-9_-]{11})", parsed_url.path)
    if match:
        return match.group(1)
    
    # Case 4: Catch any 11-char YouTube ID pattern
    match = re.search(r"([a-zA-Z0-9_-]{11})", url)
    if match:
        return match.group(1)
    
    return None

def get_transcript_anything(url: str):
  transcript = supadata.transcript(url=url)
  content = transcript.content
  total_transcript = ""
  for transcript_section in content:
    total_transcript += f"{transcript_section.text} "
  return total_transcript

def get_transcript_instagram_reel_raw(url: str):
  transcript = supadata.transcript(url=url)
  content = transcript.content
  return content

def get_transcript_v2(video_id):
  obj = ytt_api.fetch(video_id)
  total_transcript = ""
  for snippet in obj.snippets:
    total_transcript += f"{snippet.text} "
  return total_transcript