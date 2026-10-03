# Architecture

## Phase 1

Webhook -> URL validation -> blog extraction through Jina AI -> normalization/content limit -> LLM generation -> structured output validation -> webhook response.

## Phase 2

Add a self-hosted Python transcript service using youtube-transcript-api. The YouTube branch will normalize transcript data into the same source_url, title, and content contract used by the blog branch.

## Design principles

- Keep source extraction separate from generation.
- Normalize all sources into one internal schema.
- Validate generated social content before returning it.
- Keep secrets out of Git.
- Add explicit error responses as the workflow matures.