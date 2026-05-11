# BACKEND_AGENT | 2026-05-10 | Singleton async Anthropic client with retry/backoff
from __future__ import annotations

import asyncio
import random
from collections.abc import AsyncGenerator

import anthropic

from app.config import settings

_semaphore: asyncio.Semaphore | None = None
_client: anthropic.AsyncAnthropic | None = None


def _get_client() -> anthropic.AsyncAnthropic:
    global _client
    if _client is None:
        _client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
    return _client


def _get_semaphore() -> asyncio.Semaphore:
    global _semaphore
    if _semaphore is None:
        _semaphore = asyncio.Semaphore(settings.api_semaphore_limit)
    return _semaphore


async def stream_completion(
    system: str,
    user: str,
    model: str = "claude-sonnet-4-6",
    max_tokens: int = 8192,
    max_retries: int = 5,
) -> AsyncGenerator[str, None]:
    client = _get_client()
    sem = _get_semaphore()

    for attempt in range(max_retries):
        try:
            async with sem:
                async with asyncio.timeout(300):
                    async with client.messages.stream(
                        model=model,
                        max_tokens=max_tokens,
                        system=system,
                        messages=[{"role": "user", "content": user}],
                    ) as stream:
                        async for text in stream.text_stream:
                            yield text
            return
        except anthropic.RateLimitError as exc:
            if attempt == max_retries - 1:
                raise
            retry_after = float(exc.response.headers.get("retry-after", 2**attempt))
            await asyncio.sleep(retry_after + random.uniform(0, 1))
        except anthropic.AuthenticationError as exc:
            raise RuntimeError(
                f"Anthropic API authentication failed — check your ANTHROPIC_API_KEY in .env. Detail: {exc}"
            ) from exc
        except anthropic.BadRequestError as exc:
            # Surface billing errors and other 400s clearly rather than crashing silently
            detail = exc.message if hasattr(exc, "message") else str(exc)
            raise RuntimeError(f"Anthropic API rejected request: {detail}") from exc
        except anthropic.APIStatusError as exc:
            if exc.status_code in (500, 529) and attempt < max_retries - 1:
                await asyncio.sleep(2**attempt + random.uniform(0, 1))
            else:
                raise
