"""WireMock helpers for the custom wire suite.

These helpers exercise the hand-authored public wrapper (``auth0.teams.Teams``)
end to end against the same WireMock instance used by the Fern-generated
``tests/wire`` suite. Keeping them here — under the ``.fernignore``-fenced
``tests/custom`` tree — means Fern regenerations can freely overwrite
``tests/wire/conftest.py`` without touching this coverage.

The WireMock container lifecycle is owned by ``tests/conftest.py``; this module
only constructs a client pointed at the running instance and queries its admin
API to assert what was received.
"""

import os
from typing import Any, Dict, List, Optional

import httpx

from auth0.teams import Teams


def wiremock_base_url() -> str:
    """Returns the WireMock base URL from the WIREMOCK_URL environment variable."""
    return os.environ.get("WIREMOCK_URL", "http://localhost:8080")


def build_public_client(test_id: str) -> Teams:
    """Builds a public-wrapper client pointed at WireMock, tagged for request tracking.

    The ``X-Test-Id`` header lets ``verify_request_count`` isolate the requests a
    single test made, which keeps assertions correct under pytest-xdist parallelism.
    """
    test_headers = {"X-Test-Id": test_id}
    return Teams(
        team_slug="wiremock",
        tenant_domain="wiremock.local",
        token="test_token",
        base_url=wiremock_base_url(),
        httpx_client=httpx.Client(headers=test_headers),
    )


def verify_request_count(
    test_id: str,
    method: str,
    url_path: str,
    query_params: Optional[Dict[str, Any]],
    expected: int,
    body_patterns: Optional[List[Dict[str, Any]]] = None,
) -> None:
    """Asserts how many requests WireMock received for a given test, method, and path.

    Args:
        test_id: Value of the ``X-Test-Id`` header used to scope the query to one test.
        method: HTTP method to match (e.g. ``"DELETE"``).
        url_path: Exact request path to match (e.g. ``"/api/members/id/tenants"``).
        query_params: Optional query parameters to match; list values become a
            WireMock ``hasExactly`` matcher, scalars an ``equalTo`` matcher.
        expected: The exact number of matching requests expected.
        body_patterns: Optional list of WireMock ``bodyPatterns`` matchers, e.g.
            ``[{"matchesJsonPath": "$.tenants[0]"}]``. Used to assert a request body
            was sent — important for endpoints that carry a body on a verb that
            normally would not (e.g. ``DELETE /api/members/{id}/tenants``).
    """
    admin_url = f"{wiremock_base_url()}/__admin"
    request_body: Dict[str, Any] = {
        "method": method,
        "urlPath": url_path,
        "headers": {"X-Test-Id": {"equalTo": test_id}},
    }
    if query_params:
        query_parameters: Dict[str, Any] = {}
        for key, value in query_params.items():
            if isinstance(value, list):
                query_parameters[key] = {"hasExactly": [{"equalTo": item} for item in value]}
            else:
                query_parameters[key] = {"equalTo": value}
        request_body["queryParameters"] = query_parameters
    if body_patterns:
        request_body["bodyPatterns"] = body_patterns

    response = httpx.post(f"{admin_url}/requests/find", json=request_body)
    assert response.status_code == 200, "Failed to query WireMock requests"
    requests_found = len(response.json().get("requests", []))
    assert requests_found == expected, f"Expected {expected} requests, found {requests_found}"
