from .conftest import get_client, verify_request_count


def test_members_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "members.list_.0"
    client = get_client(test_id)
    client.members.list(
        take=1,
        from_="from",
    )
    verify_request_count(test_id, "GET", "/api/members", {"take": "1", "from": "from"}, 1)


def test_members_invite() -> None:
    """Test invite endpoint with WireMock"""
    test_id = "members.invite.0"
    client = get_client(test_id)
    client.members.invite(
        email="jane.smith@company.com",
        role="teams_contributor",
        tenant_ids=["538c9e21-e3d5-4ad6-b3d0-352c62369fb0", "b1c9e21e-1234-4ad6-b3d0-352c6236abcd"],
        tenant_roles=["owner", "editor-users"],
        client_ids=["client_123", "client_456"],
    )
    verify_request_count(test_id, "POST", "/api/members", None, 1)


def test_members_get() -> None:
    """Test get endpoint with WireMock"""
    test_id = "members.get.0"
    client = get_client(test_id)
    client.members.get(
        id="id",
    )
    verify_request_count(test_id, "GET", "/api/members/id", None, 1)


def test_members_delete() -> None:
    """Test delete endpoint with WireMock"""
    test_id = "members.delete.0"
    client = get_client(test_id)
    client.members.delete(
        id="id",
    )
    verify_request_count(test_id, "DELETE", "/api/members/id", None, 1)


def test_members_update() -> None:
    """Test update endpoint with WireMock"""
    test_id = "members.update.0"
    client = get_client(test_id)
    client.members.update(
        id="id",
        role="teams_owner",
    )
    verify_request_count(test_id, "PATCH", "/api/members/id", None, 1)
