"""Wire tests that drive the public ``auth0.teams.Teams`` wrapper against WireMock.

The Fern-generated ``tests/wire`` suite exercises the raw generated client. This
module covers the integration surface real integrators use — the hand-authored
public wrapper — and asserts request bodies where they matter, notably the
``DELETE`` endpoint that carries a JSON body.

Lives under ``tests/custom`` (fenced by ``.fernignore``) so it survives Fern
regenerations of ``tests/wire``.
"""

from .wire_support import build_public_client, verify_request_count


def test_members_list_routes_and_forwards_query_params() -> None:
    test_id = "custom.members.list.0"
    client = build_public_client(test_id)
    client.members.list(take=1, from_="from")
    verify_request_count(test_id, "GET", "/api/members", {"take": "1", "from": "from"}, 1)


def test_members_invite_posts_body() -> None:
    test_id = "custom.members.invite.0"
    client = build_public_client(test_id)
    client.members.invite(
        email="jane.smith@company.com",
        role="teams_contributor",
        tenant_ids=["538c9e21-e3d5-4ad6-b3d0-352c62369fb0"],
        tenant_roles=["owner"],
        client_ids=["client_123"],
    )
    verify_request_count(
        test_id,
        "POST",
        "/api/members",
        None,
        1,
        body_patterns=[{"matchesJsonPath": "$.email"}, {"matchesJsonPath": "$.role"}],
    )


def test_members_tenants_create_puts_body() -> None:
    test_id = "custom.members.tenants.create.0"
    client = build_public_client(test_id)
    client.members.tenants.create(
        id="id",
        tenants=["538c9e21-e3d5-4ad6-b3d0-352c62369fb0"],
        roles=["owner"],
        client_ids=["client_123"],
    )
    verify_request_count(
        test_id,
        "PUT",
        "/api/members/id/tenants",
        None,
        1,
        body_patterns=[{"matchesJsonPath": "$.tenants[0]"}],
    )


def test_members_tenants_remove_sends_body_on_delete() -> None:
    test_id = "custom.members.tenants.remove.0"
    client = build_public_client(test_id)
    client.members.tenants.remove(id="id", tenants=["538c9e21-e3d5-4ad6-b3d0-352c62369fb0"])
    verify_request_count(
        test_id,
        "DELETE",
        "/api/members/id/tenants",
        None,
        1,
        body_patterns=[{"matchesJsonPath": "$.tenants[0]"}],
    )


def test_tenants_delete_routes() -> None:
    test_id = "custom.tenants.delete.0"
    client = build_public_client(test_id)
    client.tenants.delete(tenant_id="tenantId")
    verify_request_count(test_id, "DELETE", "/api/tenants/tenantId", None, 1)


def test_environments_list_routes() -> None:
    test_id = "custom.environments.list.0"
    client = build_public_client(test_id)
    client.environments.list()
    verify_request_count(test_id, "GET", "/api/environments", None, 1)
