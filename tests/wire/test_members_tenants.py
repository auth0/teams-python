from .conftest import get_client, verify_request_count


def test_members_tenants_create() -> None:
    """Test create endpoint with WireMock"""
    test_id = "members.tenants.create.0"
    client = get_client(test_id)
    client.members.tenants.create(
        id="id",
        tenants=["538c9e21-e3d5-4ad6-b3d0-352c62369fb0", "b1c9e21e-1234-4ad6-b3d0-352c6236abcd"],
        roles=["owner", "editor-specific-apps"],
        client_ids=["client_123", "client_456"],
    )
    verify_request_count(test_id, "PUT", "/api/members/id/tenants", None, 1)


def test_members_tenants_remove() -> None:
    """Test remove endpoint with WireMock"""
    test_id = "members.tenants.remove.0"
    client = get_client(test_id)
    client.members.tenants.remove(
        id="id",
        tenants=["tenants"],
    )
    verify_request_count(test_id, "DELETE", "/api/members/id/tenants", None, 1)


def test_members_tenants_update() -> None:
    """Test update endpoint with WireMock"""
    test_id = "members.tenants.update.0"
    client = get_client(test_id)
    client.members.tenants.update(
        id="id",
        tenants=["538c9e21-e3d5-4ad6-b3d0-352c62369fb0"],
        roles=["owner", "editor-specific-apps"],
        client_ids=["client_123", "client_456"],
    )
    verify_request_count(test_id, "PATCH", "/api/members/id/tenants", None, 1)


def test_members_tenants_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "members.tenants.list_.0"
    client = get_client(test_id)
    client.members.tenants.list(
        id="id",
        environment="environment",
    )
    verify_request_count(test_id, "GET", "/api/members/id/tenants/environment", None, 1)
