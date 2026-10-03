# AI Content Repurposer

An n8n automation that turns blog articles and YouTube videos into reusable social content.

## Phase 1: Blog → Social Content

The current workflow accepts a POST request containing a URL and optional tone, extracts the article through Jina AI, normalizes the source, sends it to an LLM, validates the generated X/Twitter thread, and returns structured JSON.

YouTube videos are now supported through the self-hosted transcript service in Phase 2.

## Phase 2: YouTube → Social Content

The YouTube branch validates the URL, calls the local FastAPI transcript service, normalizes the transcript into the same source format used by blog articles, and sends it through the existing LLM pipeline.

Supported YouTube URL forms:
- Standard watch URLs
- `youtu.be` links
- Shorts URLs
- Embed URLs

If a transcript is unavailable, the transcript service returns HTTP 422 instead of generating content from missing source material.

### Local services

```text
n8n                 http://localhost:5678
transcript-service  internal Docker network :8000
PostgreSQL          internal Docker network :5432
```

### Request

```json
{
  "url": "https://example.com/article",
  "tone": "professional"
}
```

### Response

```json
{
  "summary": "string",
  "linkedin_post": "string",
  "tweet_thread": ["string", "..."]
}
```

## Architecture

```text
Webhook
  ↓
YouTube? ── yes → Phase 2 transcript service
  ↓ no
Validate Request
  ↓
Jina AI Article Extraction
  ↓
Normalize + 12k-word safety limit
  ↓
LLM JSON generation
  ↓
Output validation
  ↓
Respond to Webhook
```

## Repository

```text
workflow/content-repurposer.json
transcript-service/app/main.py
transcript-service/requirements.txt
transcript-service/Dockerfile
transcript-service/README.md
prompts/summary.txt
prompts/linkedin.txt
prompts/twitter.txt
docs/architecture.md
docker-compose.yml
.env.example
```

## Local setup

1. Copy `.env.example` to `.env`.
2. Add your LLM API key to the environment used by n8n.
3. Run `docker compose up -d`.
4. Open n8n at `http://localhost:5678`.
5. Import `workflow/content-repurposer.json`.
6. Test the webhook with a blog URL and a YouTube URL.
7. Activate only after testing the webhook end-to-end.

## Roadmap

- [x] Repository scaffold
- [x] Webhook input
- [x] Blog extraction via Jina AI
- [x] Source normalization and content limit
- [x] LLM JSON generation
- [x] X/Twitter character validation
- [x] Self-hosted YouTube transcript service
- [ ] Long-content chunking
- [ ] Retry/regeneration for invalid social posts
- [ ] Centralized error handling
- [ ] Google Sheets / Telegram output
- [ ] Automated tests and screenshots

### Test the transcript service

After Docker starts, the transcript service is intentionally internal to the Docker network. To test it directly from the host, temporarily publish port 8000 in docker-compose.

PowerShell health check:

    Invoke-RestMethod http://localhost:8000/health

### Test the n8n webhook

In n8n, import the workflow and use the Webhook node's Test URL.

Example request body:

    {
      "url": "https://www.youtube.com/watch?v=VIDEO_ID",
      "tone": "professional"
    }

Expected response shape:

    {
      "summary": "...",
      "linkedin_post": "...",
      "tweet_thread": ["...", "..."]
    }

For the YouTube test, use a public video with an accessible transcript. A missing transcript should produce an explicit 422 error rather than silently generating content.
