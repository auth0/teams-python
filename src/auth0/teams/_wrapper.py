from __future__ import annotations

import base64
import ipaddress
import typing
import urllib.parse
from json import dumps

import httpx

from auth0.teams.client import AsyncTeams as AsyncTeamsRawClient  # noqa: F401
from auth0.teams.client import Teams as TeamsRawClient  # noqa: F401
from auth0.teams.core.logging import LogConfig, Logger
from auth0.teams.token_provider import AsyncM2MTokenProvider, M2MTokenProvider

if typing.TYPE_CHECKING:
    from auth0.teams.activity.client import ActivityClient, AsyncActivityClient
    from auth0.teams.environments.client import AsyncEnvironmentsClient, EnvironmentsClient
    from auth0.teams.members.client import AsyncMembersClient, MembersClient
    from auth0.teams.tenants.client import AsyncTenantsClient, TenantsClient


def _validate_credentials(
    *,
    token: typing.Optional[typing.Union[str, typing.Callable[[], str]]],
    client_id: typing.Optional[str],
    client_secret: typing.Optional[str],
    tenant_domain: typing.Optional[str],
) -> None:
    has_token = token is not None
    has_credentials = client_id is not None and client_secret is not None
    if has_token == has_credentials:
        raise ValueError("auth0: provide either 'token' or both 'client_id' and 'client_secret'")
    if has_credentials and tenant_domain is None:
        raise ValueError("auth0: 'tenant_domain' is required when using 'client_id'/'client_secret'")


def _is_loopback_host(hostname: str) -> bool:
    if hostname == "localhost":
        return True
    try:
        return ipaddress.ip_address(hostname).is_loopback
    except ValueError:
        return False


def _require_non_prod_domain(param_name: str, url: str) -> None:
    non_prod_domain_suffix = "sus.auth0.com"
    hostname = urllib.parse.urlparse(url).hostname
    if hostname is not None and _is_loopback_host(hostname):
        return
    is_non_prod = hostname is not None and (
        hostname == non_prod_domain_suffix or hostname.endswith(f".{non_prod_domain_suffix}")
    )
    if not is_non_prod:
        raise ValueError(
            f"auth0: '{param_name}' override is only permitted for loopback hosts "
            f"(localhost/127.0.0.1/::1) or non-prod domains ending with "
            f"'{non_prod_domain_suffix}'; got {url!r}"
        )


def _derive_urls(
    team_slug: str,
    tenant_domain: typing.Optional[str],
    *,
    base_url: typing.Optional[str],
    audience: typing.Optional[str],
) -> typing.Tuple[str, typing.Optional[str], str]:
    if base_url is not None:
        _require_non_prod_domain("base_url", base_url)
        resolved_base_url = base_url
    else:
        resolved_base_url = f"https://{team_slug}.teams.auth0.com"
    token_url = f"https://{tenant_domain}/oauth/token" if tenant_domain is not None else None
    if audience is not None:
        _require_non_prod_domain("audience", audience)
        resolved_audience = audience
    else:
        resolved_audience = f"https://{team_slug}.teams.auth0.com/api/"
    return resolved_base_url, token_url, resolved_audience


def _merge_client_info(
    headers: typing.Optional[typing.Dict[str, str]],
    client_info: typing.Optional[typing.Dict[str, typing.Any]],
) -> typing.Optional[typing.Dict[str, str]]:
    if client_info is None:
        return headers
    encoded = base64.b64encode(dumps(client_info, separators=(",", ":")).encode("utf-8")).decode()
    return {**(headers or {}), "Auth0-Client": encoded}


class Teams:
    """
    Auth0 Teams API client with automatic token management.

    Supports two authentication modes:

    1. With an existing token (a static string or a callable that returns one)::

        client = Teams(
            team_slug="acme",
            token="YOUR_TOKEN",
        )

    2. With client credentials (automatic token acquisition and refresh)::

        client = Teams(
            team_slug="acme",
            tenant_domain="acme.us.auth0.com",
            client_id="YOUR_CLIENT_ID",
            client_secret="YOUR_CLIENT_SECRET",
        )

    Parameters
    ----------
    team_slug : str
        Your Teams slug, used to derive the API base URL and audience.
    tenant_domain : Optional[str]
        Your Auth0 tenant domain (e.g. "acme.us.auth0.com"), used as the
        OAuth token endpoint host for client-credentials authentication.
        Required when using client_id/client_secret; not needed when a token
        is provided directly.
    token : Optional[Union[str, Callable[[], str]]]
        A static bearer token or a callable that returns one. Required when
        client credentials are not provided.
    client_id : Optional[str]
        Auth0 application client ID. Required together with client_secret for
        automatic token acquisition.
    client_secret : Optional[str]
        Auth0 application client secret. Required together with client_id.
    audience : Optional[str]
        The API audience. Defaults to https://{team_slug}.teams.auth0.com/api/.
        An override is only permitted for non-prod domains (must end with
        "sus.auth0.com") and is intended for testing; raises ValueError otherwise.
    base_url : Optional[str]
        Override the derived API base URL. Only permitted for non-prod domains
        (must end with "sus.auth0.com") and is intended for testing; raises
        ValueError otherwise.
    headers : Optional[Dict[str, str]]
        Additional headers to send with every request.
    client_info : Optional[Dict[str, Any]]
        Override the Auth0-Client telemetry header. Intended for SDKs that wrap
        this one (e.g. {"name": "my-wrapper", "version": "1.0"}); the dict is
        JSON-encoded and base64-encoded into the Auth0-Client header.
    timeout : Optional[float]
        Request timeout in seconds. Defaults to 60.
    max_retries : Optional[int]
        The default maximum number of retries for failed requests. Defaults to
        2. Per-request `max_retries` in `request_options` takes precedence.
    httpx_client : Optional[httpx.Client]
        Custom httpx client for requests.
    logging : Optional[Union[LogConfig, Logger]]
        SDK logging configuration.

    Raises
    ------
    ValueError
        If neither token nor both client credentials are provided, or if
        base_url/audience is overridden with a domain that isn't a non-prod
        domain (must end with "sus.auth0.com").
    """

    def __init__(
        self,
        *,
        team_slug: str,
        tenant_domain: typing.Optional[str] = None,
        token: typing.Optional[typing.Union[str, typing.Callable[[], str]]] = None,
        client_id: typing.Optional[str] = None,
        client_secret: typing.Optional[str] = None,
        audience: typing.Optional[str] = None,
        base_url: typing.Optional[str] = None,
        headers: typing.Optional[typing.Dict[str, str]] = None,
        client_info: typing.Optional[typing.Dict[str, typing.Any]] = None,
        timeout: typing.Optional[float] = None,
        max_retries: typing.Optional[int] = None,
        httpx_client: typing.Optional[httpx.Client] = None,
        logging: typing.Optional[typing.Union[LogConfig, Logger]] = None,
    ) -> None:
        _validate_credentials(
            token=token, client_id=client_id, client_secret=client_secret, tenant_domain=tenant_domain
        )
        resolved_base_url, token_url, resolved_audience = _derive_urls(
            team_slug, tenant_domain, base_url=base_url, audience=audience
        )
        if token is None:
            token = M2MTokenProvider(
                token_url=token_url,  # type: ignore[arg-type]
                client_id=client_id,  # type: ignore[arg-type]
                client_secret=client_secret,  # type: ignore[arg-type]
                audience=resolved_audience,
            )
        self._api = TeamsRawClient(
            base_url=resolved_base_url,
            token=token,
            headers=_merge_client_info(headers, client_info),
            timeout=timeout,
            max_retries=max_retries,
            httpx_client=httpx_client,
            logging=logging,
        )

    @property
    def members(self) -> MembersClient:
        return self._api.members

    @property
    def tenants(self) -> TenantsClient:
        return self._api.tenants

    @property
    def environments(self) -> EnvironmentsClient:
        return self._api.environments

    @property
    def activity(self) -> ActivityClient:
        return self._api.activity


class AsyncTeams:
    """
    Async Auth0 Teams API client with automatic token management.

    See :class:`Teams` for the authentication modes and parameters.
    """

    def __init__(
        self,
        *,
        team_slug: str,
        tenant_domain: typing.Optional[str] = None,
        token: typing.Optional[typing.Union[str, typing.Callable[[], str]]] = None,
        client_id: typing.Optional[str] = None,
        client_secret: typing.Optional[str] = None,
        audience: typing.Optional[str] = None,
        base_url: typing.Optional[str] = None,
        headers: typing.Optional[typing.Dict[str, str]] = None,
        client_info: typing.Optional[typing.Dict[str, typing.Any]] = None,
        timeout: typing.Optional[float] = None,
        max_retries: typing.Optional[int] = None,
        httpx_client: typing.Optional[httpx.AsyncClient] = None,
        logging: typing.Optional[typing.Union[LogConfig, Logger]] = None,
    ) -> None:
        _validate_credentials(
            token=token, client_id=client_id, client_secret=client_secret, tenant_domain=tenant_domain
        )
        resolved_base_url, token_url, resolved_audience = _derive_urls(
            team_slug, tenant_domain, base_url=base_url, audience=audience
        )
        resolved_headers = _merge_client_info(headers, client_info)
        if token is None:
            self._api = AsyncTeamsRawClient(
                base_url=resolved_base_url,
                token="",
                async_token=AsyncM2MTokenProvider(
                    token_url=token_url,  # type: ignore[arg-type]
                    client_id=client_id,  # type: ignore[arg-type]
                    client_secret=client_secret,  # type: ignore[arg-type]
                    audience=resolved_audience,
                ),
                headers=resolved_headers,
                timeout=timeout,
                max_retries=max_retries,
                httpx_client=httpx_client,
                logging=logging,
            )
        else:
            self._api = AsyncTeamsRawClient(
                base_url=resolved_base_url,
                token=token,
                headers=resolved_headers,
                timeout=timeout,
                max_retries=max_retries,
                httpx_client=httpx_client,
                logging=logging,
            )

    @property
    def members(self) -> AsyncMembersClient:
        return self._api.members

    @property
    def tenants(self) -> AsyncTenantsClient:
        return self._api.tenants

    @property
    def environments(self) -> AsyncEnvironmentsClient:
        return self._api.environments

    @property
    def activity(self) -> AsyncActivityClient:
        return self._api.activity
