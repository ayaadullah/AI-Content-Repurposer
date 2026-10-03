# AI Content Repurposer

An n8n automation that turns blog articles and YouTube videos into reusable social content.

## Phase 1: Blog → Social Content

The current workflow accepts a POST request containing a URL and optional tone, extracts the article through Jina AI, normalizes the source, sends it to an LLM, validates the generated X/Twitter thread, and returns structured JSON.

YouTube transcript extraction is isolated as Phase 2.

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
6. Activate only after testing the webhook end-to-end.

## Roadmap

- [x] Repository scaffold
- [x] Webhook input
- [x] Blog extraction via Jina AI
- [x] Source normalization and content limit
- [x] LLM JSON generation
- [x] X/Twitter character validation
- [ ] Self-hosted YouTube transcript service
- [ ] Long-content chunking
- [ ] Retry/regeneration for invalid social posts
- [ ] Centralized error handling
- [ ] Google Sheets / Telegram output
- [ ] Automated tests and screenshots
