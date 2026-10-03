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
