import asyncio
import threading
import time
import typing

import httpx

LEEWAY_SECONDS = 10


class M2MTokenProvider:
    """
    Sync token provider with caching and automatic refresh.

    Fetches tokens via the OAuth 2.0 client credentials grant and caches them
    until shortly before they expire (a ``LEEWAY_SECONDS`` safety margin).

    Thread-safe: a lock prevents concurrent token fetches.
    """

    def __init__(
        self,
        *,
        token_url: str,
        client_id: str,
        client_secret: str,
        audience: str,
    ) -> None:
        self._token_url = token_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._audience = audience
        self._access_token: typing.Optional[str] = None
        self._expires_at: float = 0.0
        self._lock = threading.Lock()

    def __call__(self) -> str:
        if self._access_token and time.time() < self._expires_at - LEEWAY_SECONDS:
            return self._access_token
        with self._lock:
            if self._access_token and time.time() < self._expires_at - LEEWAY_SECONDS:
                return self._access_token
            return self._fetch()

    def _fetch(self) -> str:
        with httpx.Client() as client:
            response = client.post(
                self._token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self._client_id,
                    "client_secret": self._client_secret,
                    "audience": self._audience,
                },
            )
            response.raise_for_status()
            data = response.json()
        access_token = data.get("access_token")
        if not access_token:
            raise ValueError("auth0: token endpoint returned an empty access_token")
        self._access_token = access_token
        self._expires_at = time.time() + data.get("expires_in", 3600)
        return access_token


class AsyncM2MTokenProvider:
    """
    Async token provider with caching and automatic refresh.

    Fetches tokens via the OAuth 2.0 client credentials grant and caches them
    until shortly before they expire (a ``LEEWAY_SECONDS`` safety margin).

    Coroutine-safe: an async lock prevents concurrent token fetches.
    """

    def __init__(
        self,
        *,
        token_url: str,
        client_id: str,
        client_secret: str,
        audience: str,
    ) -> None:
        self._token_url = token_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._audience = audience
        self._access_token: typing.Optional[str] = None
        self._expires_at: float = 0.0
        self._lock = asyncio.Lock()

    async def __call__(self) -> str:
        if self._access_token and time.time() < self._expires_at - LEEWAY_SECONDS:
            return self._access_token
        async with self._lock:
            if self._access_token and time.time() < self._expires_at - LEEWAY_SECONDS:
                return self._access_token
            return await self._fetch()

    async def _fetch(self) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self._token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self._client_id,
                    "client_secret": self._client_secret,
                    "audience": self._audience,
                },
            )
            response.raise_for_status()
            data = response.json()
        access_token = data.get("access_token")
        if not access_token:
            raise ValueError("auth0: token endpoint returned an empty access_token")
        self._access_token = access_token
        self._expires_at = time.time() + data.get("expires_in", 3600)
        return access_token
