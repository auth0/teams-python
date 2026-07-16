from .conftest import get_client, verify_request_count


def test_tenants_members_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "tenants.members.list_.0"
    client = get_client(test_id)
    client.tenants.members.list(
        tenant_id="tenantId",
        take=1,
        from_="from",
    )
    verify_request_count(test_id, "GET", "/api/tenants/tenantId/members", {"take": "1", "from": "from"}, 1)
