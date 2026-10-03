# YouTube Transcript Service

Small self-hosted FastAPI service used by the AI Content Repurposer n8n workflow.

## Endpoints

### Health

GET /health

### Transcript

POST /transcript

Request:

    {
      "url": "https://www.youtube.com/watch?v=VIDEO_ID"
    }

Response:

    {
      "source_url": "https://www.youtube.com/watch?v=VIDEO_ID",
      "title": "YouTube video VIDEO_ID",
      "content": "Transcript text..."
    }

The service supports standard watch URLs, youtu.be links, Shorts URLs, and embed URLs.

A video must have an accessible transcript. Videos without an available transcript return HTTP 422.

## Local smoke test

If port 8000 is temporarily published to the host, run:

PowerShell:

    Invoke-RestMethod http://localhost:8000/health

Then:

    Invoke-RestMethod -Method Post -Uri http://localhost:8000/transcript -ContentType 'application/json' -Body '{"url":"https://www.youtube.com/watch?v=VIDEO_ID","tone":"professional"}'

Replace VIDEO_ID with a real public YouTube video that has captions/transcript access.
