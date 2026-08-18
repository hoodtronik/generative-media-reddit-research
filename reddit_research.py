"""Minimal, read-only Reddit research client for a local generative-media assistant.

Requires Reddit Data API approval and valid OAuth application credentials.
Credentials are read from environment variables and are never stored in source.
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Any

import requests

TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
API_BASE = "https://oauth.reddit.com"


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def get_access_token() -> tuple[str, str]:
    client_id = required_env("REDDIT_CLIENT_ID")
    client_secret = required_env("REDDIT_CLIENT_SECRET")
    user_agent = required_env("REDDIT_USER_AGENT")

    response = requests.post(
        TOKEN_URL,
        auth=(client_id, client_secret),
        data={"grant_type": "client_credentials"},
        headers={"User-Agent": user_agent},
        timeout=20,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["access_token"], user_agent


def search_subreddit(subreddit: str, query: str, limit: int = 10) -> list[dict[str, Any]]:
    token, user_agent = get_access_token()
    response = requests.get(
        f"{API_BASE}/r/{subreddit}/search",
        headers={
            "Authorization": f"bearer {token}",
            "User-Agent": user_agent,
        },
        params={
            "q": query,
            "restrict_sr": "true",
            "sort": "new",
            "t": "month",
            "limit": max(1, min(limit, 25)),
            "raw_json": 1,
        },
        timeout=20,
    )
    response.raise_for_status()

    results: list[dict[str, Any]] = []
    for child in response.json().get("data", {}).get("children", []):
        data = child.get("data", {})
        results.append(
            {
                "title": data.get("title", ""),
                "score": data.get("score", 0),
                "author": data.get("author", ""),
                "permalink": "https://www.reddit.com" + data.get("permalink", ""),
                "text_preview": (data.get("selftext") or "")[:400],
            }
        )
    return results


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Search a selected public subreddit for generative-media research."
    )
    parser.add_argument("--subreddit", required=True)
    parser.add_argument("--query", required=True)
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    try:
        results = search_subreddit(args.subreddit, args.query, args.limit)
    except (RuntimeError, requests.RequestException, KeyError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not results:
        print("No matching posts found.")
        return 0

    for index, item in enumerate(results, start=1):
        print(f"\n{index}. {item['title']}")
        print(f"   Score: {item['score']} | Author: u/{item['author']}")
        print(f"   {item['permalink']}")
        if item["text_preview"]:
            print(f"   {item['text_preview']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
