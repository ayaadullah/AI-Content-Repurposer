# Architecture

## Phase 1 + Phase 2

The workflow accepts one source URL and routes it by source type.

```text
Webhook
   |
   v
YouTube?
   | yes                         | no
   v                             v
Validate YouTube URL       Validate Request
   |                             |
   v                             v
Transcript Service          Jina AI Extraction
   |                             |
   +-------------+---------------+
                 |
                 v
          Normalize + 12k-word limit
                 |
                 v
            LLM generation
                 |
                 v
          Output validation
                 |
                 v
          Webhook response
```

## Transcript service

The self-hosted service lives in `transcript-service/` and exposes:

- `GET /health`
- `POST /transcript`

It extracts a YouTube video ID, requests the available transcript through `youtube-transcript-api`, joins transcript snippets into plain text, and returns:

```json
{
  "source_url": "https://www.youtube.com/watch?v=...",
  "title": "YouTube video ...",
  "content": "..."
}
```

The n8n container reaches it through the Docker service name:

```text
http://transcript-service:8000/transcript
```

## Reliability boundaries

- Validate URLs before extraction.
- Reject unsupported source URLs.
- Return an explicit error when a transcript is unavailable.
- Cap source material at 12,000 words before the LLM.
- Require JSON-shaped LLM output.
- Reject X/Twitter posts longer than 280 characters.
