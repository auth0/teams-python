import base64
import json

import httpx
import pytest

from auth0.teams import AsyncTeams, Teams
from auth0.teams.activity.client import ActivityClient, AsyncActivityClient
from auth0.teams.environments.client import AsyncEnvironmentsClient, EnvironmentsClient
from auth0.teams.members.client import AsyncMembersClient, MembersClient
from auth0.teams.tenants.client import AsyncTenantsClient, TenantsClient
from auth0.teams.token_provider import AsyncM2MTokenProvider, M2MTokenProvider


def test_teams_static_token_constructs() -> None:
    client = Teams(team_slug="acme", token="tok")
    assert isinstance(client.members, MembersClient)
    assert isinstance(client.tenants, TenantsClient)
    assert isinstance(client.environments, EnvironmentsClient)
    assert isinstance(client.activity, ActivityClient)


def test_teams_callable_token_constructs() -> None:
    client = Teams(team_slug="acme", tenant_domain="acme.us.auth0.com", token=lambda: "tok")
    assert isinstance(client.tenants, TenantsClient)


def test_teams_client_credentials_builds_provider() -> None:
    client = Teams(
        team_slug="acme",
        tenant_domain="acme.us.auth0.com",
        client_id="id",
        client_secret="secret",
    )
    provider = client._api._client_wrapper._token
    assert isinstance(provider, M2MTokenProvider)
    assert provider._token_url == "https://acme.us.auth0.com/oauth/token"
    assert provider._audience == "https://acme.teams.auth0.com/api/"


def test_teams_no_auth_raises() -> None:
    with pytest.raises(ValueError, match="provide either 'token'"):
        Teams(team_slug="acme", tenant_domain="acme.us.auth0.com")


def test_teams_both_auth_modes_raises() -> None:
    with pytest.raises(ValueError, match="provide either 'token'"):
        Teams(
            team_slug="acme",
            tenant_domain="acme.us.auth0.com",
            token="tok",
            client_id="id",
            client_secret="secret",
        )


def test_teams_client_credentials_without_tenant_domain_raises() -> None:
    with pytest.raises(ValueError, match="'tenant_domain' is required"):
        Teams(team_slug="acme", client_id="id", client_secret="secret")


def test_teams_static_token_without_tenant_domain_constructs() -> None:
    client = Teams(team_slug="acme", token="tok")
    assert isinstance(client.tenants, TenantsClient)


def test_teams_derives_base_url() -> None:
    client = Teams(team_slug="acme", tenant_domain="acme.us.auth0.com", token="tok")
    assert client._api._client_wrapper.get_base_url() == "https://acme.teams.auth0.com"


def test_teams_base_url_override() -> None:
    client = Teams(
        team_slug="acme",
        tenant_domain="acme.us.auth0.com",
        token="tok",
        base_url="https://override.sus.auth0.com",
    )
    assert client._api._client_wrapper.get_base_url() == "https://override.sus.auth0.com"


def test_teams_base_url_override_rejects_non_prod_domain() -> None:
    with pytest.raises(ValueError, match="'base_url' override is only permitted"):
        Teams(
            team_slug="acme",
            tenant_domain="acme.us.auth0.com",
            token="tok",
            base_url="https://override.example.com",
        )


def test_teams_audience_override_used_in_provider() -> None:
    client = Teams(
        team_slug="acme",
        tenant_domain="acme.us.auth0.com",
        client_id="id",
        client_secret="secret",
        audience="https://custom-audience.sus.auth0.com/api",
    )
    provider = client._api._client_wrapper._token
    assert isinstance(provider, M2MTokenProvider)
    assert provider._audience == "https://custom-audience.sus.auth0.com/api"


def test_teams_audience_override_rejects_non_prod_domain() -> None:
    with pytest.raises(ValueError, match="'audience' override is only permitted"):
        Teams(
            team_slug="acme",
            tenant_domain="acme.us.auth0.com",
            client_id="id",
            client_secret="secret",
            audience="https://custom-audience/api",
        )


@pytest.mark.parametrize(
    "base_url",
    [
        "http://localhost:8080",
        "http://localhost",
        "http://127.0.0.1:8080",
        "http://[::1]:8080",
    ],
)
def test_teams_base_url_override_allows_loopback(base_url: str) -> None:
    client = Teams(team_slug="acme", tenant_domain="acme.us.auth0.com", token="tok", base_url=base_url)
    assert client._api._client_wrapper.get_base_url() == base_url


@pytest.mark.parametrize(
    "base_url",
    [
        "https://localhost.example.com",
        "http://notlocalhost",
        "https://evilsus.auth0.com",
        "https://sus.auth0.com.evil.com",
    ],
)
def test_teams_base_url_override_rejects_loopback_and_suffix_spoofing(base_url: str) -> None:
    with pytest.raises(ValueError, match="'base_url' override is only permitted"):
        Teams(team_slug="acme", tenant_domain="acme.us.auth0.com", token="tok", base_url=base_url)


def test_auth0_client_header_present_and_well_formed() -> None:
    client = Teams(team_slug="acme", tenant_domain="acme.us.auth0.com", token="tok")
    headers = client._api._client_wrapper.get_headers()
    assert "Auth0-Client" in headers
    decoded = json.loads(base64.b64decode(headers["Auth0-Client"]).decode())
    assert decoded["name"] == "auth0-teams-python"
    assert "python" in decoded["env"]


def test_no_x_fern_headers() -> None:
    client = Teams(team_slug="acme", tenant_domain="acme.us.auth0.com", token="tok")
    headers = client._api._client_wrapper.get_headers()
    assert [k for k in headers if k.startswith("X-Fern-")] == []


def test_user_agent_matches_python_references() -> None:
    import platform

    client = Teams(team_slug="acme", tenant_domain="acme.us.auth0.com", token="tok")
    headers = client._api._client_wrapper.get_headers()
    assert headers["User-Agent"] == f"Python/{platform.python_version()}"


def test_client_info_overrides_auth0_client_header() -> None:
    client = Teams(
        team_slug="acme",
        tenant_domain="acme.us.auth0.com",
        token="tok",
        client_info={"name": "my-wrapper", "version": "1.0"},
    )
    headers = client._api._client_wrapper.get_headers()
    decoded = json.loads(base64.b64decode(headers["Auth0-Client"]).decode())
    assert decoded == {"name": "my-wrapper", "version": "1.0"}


def test_providers_exported_from_package() -> None:
    from auth0.teams import AsyncM2MTokenProvider as ExportedAsync
    from auth0.teams import M2MTokenProvider as ExportedSync

    assert ExportedSync is M2MTokenProvider
    assert ExportedAsync is AsyncM2MTokenProvider


def test_authorization_header_uses_token() -> None:
    client = Teams(team_slug="acme", tenant_domain="acme.us.auth0.com", token="mytoken")
    headers = client._api._client_wrapper.get_headers()
    assert headers["Authorization"] == "Bearer mytoken"


def test_async_teams_static_token_constructs() -> None:
    client = AsyncTeams(team_slug="acme", tenant_domain="acme.us.auth0.com", token="tok")
    assert isinstance(client.members, AsyncMembersClient)
    assert isinstance(client.tenants, AsyncTenantsClient)
    assert isinstance(client.environments, AsyncEnvironmentsClient)
    assert isinstance(client.activity, AsyncActivityClient)


def test_async_teams_client_credentials_builds_async_provider() -> None:
    client = AsyncTeams(
        team_slug="acme",
        tenant_domain="acme.us.auth0.com",
        client_id="id",
        client_secret="secret",
    )
    assert isinstance(client._api._client_wrapper._async_token, AsyncM2MTokenProvider)


def test_async_teams_no_auth_raises() -> None:
    with pytest.raises(ValueError, match="provide either 'token'"):
        AsyncTeams(team_slug="acme", tenant_domain="acme.us.auth0.com")


def test_teams_imported_from_package() -> None:
    from auth0.teams import Teams as T

    assert T is Teams


def test_teams_raw_client_is_available() -> None:
    from auth0.teams import TeamsRawClient

    assert TeamsRawClient is not None
    assert TeamsRawClient is not Teams


def test_teams_accepts_custom_httpx_client() -> None:
    external = httpx.Client()
    client = Teams(
        team_slug="acme",
        tenant_domain="acme.us.auth0.com",
        token="tok",
        httpx_client=external,
    )
    assert isinstance(client.members, MembersClient)
    external.close()
