import re
from urllib.parse import parse_qs, urlparse

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from youtube_transcript_api import YouTubeTranscriptApi

app = FastAPI(title="AI Content Repurposer Transcript Service", version="1.0.0")


class TranscriptRequest(BaseModel):
    url: HttpUrl


def extract_video_id(url: str) -> str:
    parsed = urlparse(url)
    host = parsed.netloc.lower().split(":")[0]

    if host in {"youtu.be", "www.youtu.be"}:
        video_id = parsed.path.strip("/").split("/")[0]
    elif host.endswith("youtube.com"):
        if parsed.path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [None])[0]
        elif parsed.path.startswith("/shorts/"):
            video_id = parsed.path.split("/shorts/", 1)[1].split("/", 1)[0]
        elif parsed.path.startswith("/embed/"):
            video_id = parsed.path.split("/embed/", 1)[1].split("/", 1)[0]
        else:
            video_id = None
    else:
        video_id = None

    if not video_id or not re.fullmatch(r"[A-Za-z0-9_-]{6,20}", video_id):
        raise ValueError("Could not extract a valid YouTube video ID.")

    return video_id


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/transcript")
def transcript(request: TranscriptRequest):
    source_url = str(request.url)

    try:
        video_id = extract_video_id(source_url)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)
        content = " ".join(
            snippet.text.strip()
            for snippet in transcript
            if snippet.text and snippet.text.strip()
        ).strip()
    except Exception as exc:
        raise HTTPException(
            status_code=422,
            detail=f"Transcript unavailable for this video: {exc}",
        ) from exc

    if not content:
        raise HTTPException(status_code=422, detail="Transcript is empty.")

    return {
        "source_url": source_url,
        "title": f"YouTube video {video_id}",
        "content": content,
    }
