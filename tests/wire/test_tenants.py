from .conftest import get_client, verify_request_count

from auth0.teams import PublicCloudPayload


def test_tenants_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "tenants.list_.0"
    client = get_client(test_id)
    client.tenants.list(
        take=1,
        from_="from",
        sort="sort",
        environment="US-3",
        environment_tag="development",
        locality="us",
    )
    verify_request_count(
        test_id,
        "GET",
        "/api/tenants",
        {
            "take": "1",
            "from": "from",
            "sort": "sort",
            "environment": "US-3",
            "environment_tag": "development",
            "locality": "us",
        },
        1,
    )


def test_tenants_create() -> None:
    """Test create endpoint with WireMock"""
    test_id = "tenants.create.0"
    client = get_client(test_id)
    client.tenants.create(
        request=PublicCloudPayload(
            admin_email="admin_email",
            locality="us",
        ),
    )
    verify_request_count(test_id, "POST", "/api/tenants", None, 1)


def test_tenants_get() -> None:
    """Test get endpoint with WireMock"""
    test_id = "tenants.get.0"
    client = get_client(test_id)
    client.tenants.get(
        tenant_id="tenantId",
    )
    verify_request_count(test_id, "GET", "/api/tenants/tenantId", None, 1)


def test_tenants_delete() -> None:
    """Test delete endpoint with WireMock"""
    test_id = "tenants.delete.0"
    client = get_client(test_id)
    client.tenants.delete(
        tenant_id="tenantId",
    )
    verify_request_count(test_id, "DELETE", "/api/tenants/tenantId", None, 1)
