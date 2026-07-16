from .conftest import get_client, verify_request_count


def test_environments_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "environments.list_.0"
    client = get_client(test_id)
    client.environments.list()
    verify_request_count(test_id, "GET", "/api/environments", None, 1)
