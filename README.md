# Generative Media Reddit Research

A small personal research integration for discovering useful public Reddit discussions about generative-media workflows.

## Purpose

This project supports a local AI-assisted video production workflow. It uses Reddit as a research source to help surface public posts and discussions about topics such as:

- Stable Diffusion workflows
- ComfyUI techniques
- LoRAs and model configuration
- AI video workflows
- MiniMax video models, including H3-related techniques
- Prompting, troubleshooting, and community tutorials

The integration is intended for personal research and discovery. It is not designed to train or fine-tune AI models on Reddit content, build or resell datasets, mass-scrape Reddit, automatically vote, send unsolicited messages, or publish automated comments or posts.

## How it works

1. A user or local agent requests research on a generative-media topic.
2. The integration queries a small set of relevant public Reddit communities using the Reddit API.
3. It retrieves matching public posts and, when needed, their public comment threads.
4. The local agent summarizes or ranks useful findings.
5. Results retain links back to the original Reddit discussions so the user can inspect the source directly.

## Scope

Initial use is limited to public communities relevant to generative-media production, such as `r/StableDiffusion`, `r/comfyui`, and closely related technical communities. Queries are topic-driven and intentionally narrow rather than broad collection of Reddit content.

## Data handling

- Reddit content is used only for personal research and discovery.
- The integration does not use Reddit content for model training or fine-tuning.
- It does not sell, redistribute, or publish Reddit-derived datasets.
- Credentials are loaded from local environment variables and are never committed to this repository.
- The integration is designed to respect Reddit API authentication requirements, rate limits, and applicable developer policies.

## Configuration

Copy `.env.example` to `.env` and provide your own approved Reddit API credentials locally.

```text
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=generative-media-reddit-research/0.1 by u/your_username
```

## Example

```bash
python reddit_research.py --subreddit StableDiffusion --query "MiniMax H3 workflow"
```

The script prints a small set of matching posts with titles, scores, URLs, and short text previews. It is intentionally a minimal reference implementation rather than a bulk archival tool.

## Development status

This repository is a public, sanitized reference implementation of the Reddit-facing research component used by a larger local creative-production system. The larger local system and unrelated personal project files are not included here.
