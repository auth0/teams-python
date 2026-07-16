import datetime

from .conftest import get_client, verify_request_count


def test_activity_list_() -> None:
    """Test list endpoint with WireMock"""
    test_id = "activity.list_.0"
    client = get_client(test_id)
    client.activity.list(
        take=1,
        from_="from",
        since=datetime.datetime.fromisoformat("2024-01-15T09:30:00+00:00"),
        until=datetime.datetime.fromisoformat("2024-01-15T09:30:00+00:00"),
        type="Team Member",
        status="Success",
    )
    verify_request_count(
        test_id,
        "GET",
        "/api/activity/logs",
        {
            "take": "1",
            "from": "from",
            "since": "2024-01-15T09:30:00Z",
            "until": "2024-01-15T09:30:00Z",
            "type": "Team Member",
            "status": "Success",
        },
        1,
    )
