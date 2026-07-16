import asyncio
import time

import httpx
import pytest
import respx

from auth0.teams.token_provider import AsyncM2MTokenProvider, M2MTokenProvider

TOKEN_URL = "https://acme.us.auth0.com/oauth/token"


def _token_response(access_token: str = "tok1", expires_in: int = 3600):
    return {"access_token": access_token, "token_type": "Bearer", "expires_in": expires_in}


def _make_provider() -> M2MTokenProvider:
    return M2MTokenProvider(
        token_url=TOKEN_URL,
        client_id="client_id",
        client_secret="client_secret",
        audience="https://acme.teams.auth0.com/api",
    )


@respx.mock
def test_fetches_token() -> None:
    respx.post(TOKEN_URL).mock(return_value=httpx.Response(200, json=_token_response("tok1")))
    assert _make_provider()() == "tok1"


@respx.mock
def test_caches_token_within_ttl() -> None:
    route = respx.post(TOKEN_URL).mock(return_value=httpx.Response(200, json=_token_response("tok1")))
    provider = _make_provider()
    provider()
    provider()
    assert route.call_count == 1


@respx.mock
def test_refreshes_on_expiry() -> None:
    route = respx.post(TOKEN_URL).mock(
        side_effect=[
            httpx.Response(200, json=_token_response("tok1", expires_in=61)),
            httpx.Response(200, json=_token_response("tok2", expires_in=3600)),
        ]
    )
    provider = _make_provider()
    assert provider() == "tok1"
    provider._expires_at = time.time() - 1
    assert provider() == "tok2"
    assert route.call_count == 2


@respx.mock
def test_empty_access_token_raises() -> None:
    respx.post(TOKEN_URL).mock(return_value=httpx.Response(200, json=_token_response("")))
    with pytest.raises(ValueError, match="empty access_token"):
        _make_provider()()


@respx.mock
def test_non_2xx_raises() -> None:
    respx.post(TOKEN_URL).mock(return_value=httpx.Response(401, json={"error": "unauthorized"}))
    with pytest.raises(httpx.HTTPStatusError):
        _make_provider()()


@respx.mock
def test_sends_client_credentials_grant() -> None:
    route = respx.post(TOKEN_URL).mock(return_value=httpx.Response(200, json=_token_response("tok1")))
    _make_provider()()
    request = route.calls.last.request
    assert b"grant_type=client_credentials" in request.content
    assert b"audience=https" in request.content


@pytest.mark.asyncio
@respx.mock
async def test_async_empty_access_token_raises() -> None:
    respx.post(TOKEN_URL).mock(return_value=httpx.Response(200, json=_token_response("")))
    provider = AsyncM2MTokenProvider(
        token_url=TOKEN_URL,
        client_id="client_id",
        client_secret="client_secret",
        audience="https://acme.teams.auth0.com/api",
    )
    with pytest.raises(ValueError, match="empty access_token"):
        await provider()


@pytest.mark.asyncio
@respx.mock
async def test_async_concurrent_calls_fetch_once() -> None:
    call_count = 0

    async def slow_response(request: httpx.Request) -> httpx.Response:
        nonlocal call_count
        call_count += 1
        await asyncio.sleep(0.05)
        return httpx.Response(200, json=_token_response("tok1"))

    respx.post(TOKEN_URL).mock(side_effect=slow_response)
    provider = AsyncM2MTokenProvider(
        token_url=TOKEN_URL,
        client_id="client_id",
        client_secret="client_secret",
        audience="https://acme.teams.auth0.com/api",
    )
    results = await asyncio.gather(provider(), provider(), provider())
    assert all(r == "tok1" for r in results)
    assert call_count == 1
