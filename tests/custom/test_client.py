import pytest

from auth0.teams import Teams


def test_client_construction_with_static_token() -> None:
    client = Teams(team_slug="acme", tenant_domain="acme.us.auth0.com", token="eyJhbGci...")
    assert client.tenants is not None
    assert client.members is not None
    assert client.environments is not None
    assert client.activity is not None


def test_client_validates_at_construction() -> None:
    with pytest.raises(ValueError):
        Teams(team_slug="acme", tenant_domain="acme.us.auth0.com")
