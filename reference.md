# Reference
## Members
<details><summary><code>client.members.<a href="src/auth0.teams/members/client.py">list</a>(...) -> ListMembersResponseContent</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This endpoint retrieves a paginated list of all members under the current team. It supports checkpoint-based pagination for efficient retrieval of large datasets
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from auth0.teams import Teams
from auth0.teams.environment import TeamsEnvironment

client = Teams(
    token="<token>",
    environment=TeamsEnvironment.DEFAULT,
)

client.members.list(
    take=1,
    from_="from",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**take:** `typing.Optional[int]` — Maximum number of items to return per page. Defaults to 50. Maximum 50
    
</dd>
</dl>

<dl>
<dd>

**from:** `typing.Optional[str]` — Checkpoint cursor for pagination; use the 'next' value from a previous response to fetch the next page
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.members.<a href="src/auth0.teams/members/client.py">invite</a>(...) -> InviteMembersResponseContent</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This endpoint invites a new member to the team and optionally grants them access to one or more tenants with specified roles
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from auth0.teams import Teams
from auth0.teams.environment import TeamsEnvironment

client = Teams(
    token="<token>",
    environment=TeamsEnvironment.DEFAULT,
)

client.members.invite(
    email="jane.smith@company.com",
    role="teams_contributor",
    tenant_ids=[
        "538c9e21-e3d5-4ad6-b3d0-352c62369fb0",
        "b1c9e21e-1234-4ad6-b3d0-352c6236abcd"
    ],
    tenant_roles=[
        "owner",
        "editor-users"
    ],
    client_ids=[
        "client_123",
        "client_456"
    ],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**email:** `str` — The email of the team member
    
</dd>
</dl>

<dl>
<dd>

**role:** `TeamMemberRoleEnum` 
    
</dd>
</dl>

<dl>
<dd>

**tenant_ids:** `typing.Optional[typing.List[TenantId]]` — Specifies an optional list of tenant IDs and their corresponding role assignments.
    
</dd>
</dl>

<dl>
<dd>

**tenant_roles:** `typing.Optional[typing.List[TenantMemberRoleEnum]]` — The list of roles for each tenant.
    
</dd>
</dl>

<dl>
<dd>

**client_ids:** `typing.Optional[typing.List[ClientId]]` — The list of apps the user has access to for the 'editor-specific-apps' role. This property is only present for this role.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.members.<a href="src/auth0.teams/members/client.py">get</a>(...) -> GetMembersResponseContent</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the team member's identity and team-level role. Tenant access is retrieved via /api/members/{id}/tenants/{environment}.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from auth0.teams import Teams
from auth0.teams.environment import TeamsEnvironment

client = Teams(
    token="<token>",
    environment=TeamsEnvironment.DEFAULT,
)

client.members.get(
    id="id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The unique ID of the team member to retrieve.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.members.<a href="src/auth0.teams/members/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This endpoint deletes a team member from the team.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from auth0.teams import Teams
from auth0.teams.environment import TeamsEnvironment

client = Teams(
    token="<token>",
    environment=TeamsEnvironment.DEFAULT,
)

client.members.delete(
    id="id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The unique ID of the team member to delete.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.members.<a href="src/auth0.teams/members/client.py">update</a>(...) -> UpdateMembersResponseContent</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This endpoint can be used to change the team-level role for the team member
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from auth0.teams import Teams
from auth0.teams.environment import TeamsEnvironment

client = Teams(
    token="<token>",
    environment=TeamsEnvironment.DEFAULT,
)

client.members.update(
    id="id",
    role="teams_owner",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The unique ID of the team member to update
    
</dd>
</dl>

<dl>
<dd>

**role:** `TeamMemberRoleEnum` — The new role to assign to the team member.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Tenants
<details><summary><code>client.tenants.<a href="src/auth0.teams/tenants/client.py">list</a>(...) -> ListTenantsResponseContent</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This endpoint retrieves a paginated list of tenants for a specified team. It supports cursor-based pagination to ensure efficient data retrieval across large datasets. If the private cloud support beta is enabled for the team, the response includes both public and private tenants; otherwise, only public tenants are returned. To navigate results, the next cursor from the response should be used to fetch subsequent pages.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from auth0.teams import Teams
from auth0.teams.environment import TeamsEnvironment

client = Teams(
    token="<token>",
    environment=TeamsEnvironment.DEFAULT,
)

client.tenants.list(
    take=1,
    from_="from",
    sort="sort",
    environment="US-3",
    environment_tag="development",
    locality="us",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**take:** `typing.Optional[int]` — Maximum number of items to return per page. Defaults to 50. Maximum 50
    
</dd>
</dl>

<dl>
<dd>

**from:** `typing.Optional[str]` — Checkpoint cursor for pagination; use the 'next' value from a previous response to fetch the next page
    
</dd>
</dl>

<dl>
<dd>

**sort:** `typing.Optional[str]` — Sort order for results using MongoDB-style syntax. Defaults to 'created_at:-1' (newest first, descending). Use 'created_at:1' for oldest first (ascending). Format: field:direction where direction is 1 (ascending) or -1 (descending).
    
</dd>
</dl>

<dl>
<dd>

**environment:** `typing.Optional[str]` — Filter tenants by environment. For public cloud tenants, use the short name (e.g., 'US-3', 'EU-1'). For private cloud tenants, use the space name (e.g., 'acme-dev').
    
</dd>
</dl>

<dl>
<dd>

**environment_tag:** `typing.Optional[EnvironmentTypeEnum]` — Filter tenants by environment tag
    
</dd>
</dl>

<dl>
<dd>

**locality:** `typing.Optional[str]` — Filter tenants by locality. For public cloud tenants, matches locality (e.g., 'us', 'eu'). For private cloud tenants, matches the space's primary locality (e.g., 'virginia', 'frankfurt').
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.tenants.<a href="src/auth0.teams/tenants/client.py">create</a>(...) -> CreateTenantsResponseContent</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This endpoint creates a new tenant under your team. Upon successful creation, the response includes the tenant's details and management client credentials. The tenant type (public or private) is determined by the attributes in the request payload. Refer to the payload schema for required attributes.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from auth0.teams import Teams, PublicCloudPayload
from auth0.teams.environment import TeamsEnvironment

client = Teams(
    token="<token>",
    environment=TeamsEnvironment.DEFAULT,
)

client.tenants.create(
    request=PublicCloudPayload(
        admin_email="admin_email",
        locality="us",
    ),
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request:** `CreateTenantsRequestContent` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.tenants.<a href="src/auth0.teams/tenants/client.py">get</a>(...) -> GetTenantsResponseContent</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This endpoint retrieves all metadata for a specific tenant, including the tenant's unique ID, name, domain, environment, locality, environment type, and creation date. It is useful for obtaining comprehensive information about a tenant for display in dashboards, auditing, or automated management tasks. The response includes all relevant fields required to identify and manage the tenant programmatically
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from auth0.teams import Teams
from auth0.teams.environment import TeamsEnvironment

client = Teams(
    token="<token>",
    environment=TeamsEnvironment.DEFAULT,
)

client.tenants.get(
    tenant_id="tenantId",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**tenant_id:** `TenantId` — The unique ID of the tenant to retrieve (UUID format)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.tenants.<a href="src/auth0.teams/tenants/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a tenant from the current team
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from auth0.teams import Teams
from auth0.teams.environment import TeamsEnvironment

client = Teams(
    token="<token>",
    environment=TeamsEnvironment.DEFAULT,
)

client.tenants.delete(
    tenant_id="tenantId",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**tenant_id:** `TenantId` — The id of the tenant to delete
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Environments
<details><summary><code>client.environments.<a href="src/auth0.teams/environments/client.py">list</a>() -> ListEnvironmentsResponseContent</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This endpoint provide a list of environments associated with the Team where tenants exist.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from auth0.teams import Teams
from auth0.teams.environment import TeamsEnvironment

client = Teams(
    token="<token>",
    environment=TeamsEnvironment.DEFAULT,
)

client.environments.list()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Activity
<details><summary><code>client.activity.<a href="src/auth0.teams/activity/client.py">list</a>(...) -> ListActivityResponseContent</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This endpoint returns a paginated list of activity log entries for the team.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from auth0.teams import Teams
from auth0.teams.environment import TeamsEnvironment
import datetime

client = Teams(
    token="<token>",
    environment=TeamsEnvironment.DEFAULT,
)

client.activity.list(
    take=1,
    from_="from",
    since=datetime.datetime.fromisoformat("2024-01-15T09:30:00+00:00"),
    until=datetime.datetime.fromisoformat("2024-01-15T09:30:00+00:00"),
    type="Team Member",
    status="Success",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**take:** `typing.Optional[int]` — Maximum number of items to return per page. Defaults to 50. Maximum 50
    
</dd>
</dl>

<dl>
<dd>

**from:** `typing.Optional[str]` — Checkpoint cursor for pagination; use the 'next' value from a previous response to fetch the next page
    
</dd>
</dl>

<dl>
<dd>

**since:** `typing.Optional[DateTimeIso]` — Return logs created at or after this ISO 8601 date format
    
</dd>
</dl>

<dl>
<dd>

**until:** `typing.Optional[DateTimeIso]` — Return logs created before this ISO 8601 timestamp
    
</dd>
</dl>

<dl>
<dd>

**type:** `typing.Optional[ActivityLogEventTypeEnum]` — Exact match: filter by event type
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[ActivityLogStatusEnum]` — Exact match: filter by status
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Members Tenants
<details><summary><code>client.members.tenants.<a href="src/auth0.teams/members/tenants/client.py">create</a>(...) -> typing.Optional[CreateMembersTenantsResponseContent]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This endpoint can be used to add new tenants access
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from auth0.teams import Teams
from auth0.teams.environment import TeamsEnvironment

client = Teams(
    token="<token>",
    environment=TeamsEnvironment.DEFAULT,
)

client.members.tenants.create(
    id="id",
    tenants=[
        "538c9e21-e3d5-4ad6-b3d0-352c62369fb0",
        "b1c9e21e-1234-4ad6-b3d0-352c6236abcd"
    ],
    roles=[
        "owner",
        "editor-specific-apps"
    ],
    client_ids=[
        "client_123",
        "client_456"
    ],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The unique ID of the team member to update
    
</dd>
</dl>

<dl>
<dd>

**tenants:** `typing.List[TenantId]` — A list of tenant ids
    
</dd>
</dl>

<dl>
<dd>

**roles:** `typing.List[TenantMemberRoleEnum]` — List of roles to be assigned to the tenant member
    
</dd>
</dl>

<dl>
<dd>

**client_ids:** `typing.Optional[typing.List[ClientId]]` — List of applications. Only if nested role is editor-specific-app
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.members.tenants.<a href="src/auth0.teams/members/tenants/client.py">remove</a>(...) -> typing.Optional[DeleteMembersTenantsResponseContent]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This endpoint can be used to remove tenant access
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from auth0.teams import Teams
from auth0.teams.environment import TeamsEnvironment

client = Teams(
    token="<token>",
    environment=TeamsEnvironment.DEFAULT,
)

client.members.tenants.remove(
    id="id",
    tenants=[
        "tenants"
    ],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The unique ID of the team member.
    
</dd>
</dl>

<dl>
<dd>

**tenants:** `typing.List[TenantId]` — Specifies list of tenant IDs to be removed
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.members.tenants.<a href="src/auth0.teams/members/tenants/client.py">update</a>(...) -> typing.Optional[UpdateMembersTenantsResponseContent]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This endpoint can be used to update existing tenant roles.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from auth0.teams import Teams
from auth0.teams.environment import TeamsEnvironment

client = Teams(
    token="<token>",
    environment=TeamsEnvironment.DEFAULT,
)

client.members.tenants.update(
    id="id",
    tenants=[
        "538c9e21-e3d5-4ad6-b3d0-352c62369fb0"
    ],
    roles=[
        "owner",
        "editor-specific-apps"
    ],
    client_ids=[
        "client_123",
        "client_456"
    ],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — The unique ID of the team member to update
    
</dd>
</dl>

<dl>
<dd>

**tenants:** `typing.List[TenantId]` — A list of tenant ids
    
</dd>
</dl>

<dl>
<dd>

**roles:** `typing.List[TenantMemberRoleEnum]` — List of roles to be assigned to the tenant member
    
</dd>
</dl>

<dl>
<dd>

**client_ids:** `typing.Optional[typing.List[ClientId]]` — List of applications. Only if nested role is editor-specific-app
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.members.tenants.<a href="src/auth0.teams/members/tenants/client.py">list</a>(...) -> ListMembersTenantsResponseContent</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This endpoint retrieves a list of all tenants within a specific environment that the team member has access to. Environment identifiers required for this request can be obtained using the /api/environments endpoint, which provides details for all environments where tenants associated with your team exists.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from auth0.teams import Teams
from auth0.teams.environment import TeamsEnvironment

client = Teams(
    token="<token>",
    environment=TeamsEnvironment.DEFAULT,
)

client.members.tenants.list(
    id="id",
    environment="environment",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — Unique ID of the team member.
    
</dd>
</dl>

<dl>
<dd>

**environment:** `str` — The cloud environment identifier (e.g. 'US-3', 'EU-1', 'acme-dev').
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Tenants Members
<details><summary><code>client.tenants.members.<a href="src/auth0.teams/tenants/members/client.py">list</a>(...) -> ListTenantsMembersResponseContent</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

This endpoint retrieves a paginated list of all members for a specific tenant.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from auth0.teams import Teams
from auth0.teams.environment import TeamsEnvironment

client = Teams(
    token="<token>",
    environment=TeamsEnvironment.DEFAULT,
)

client.tenants.members.list(
    tenant_id="tenantId",
    take=1,
    from_="from",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**tenant_id:** `TenantId` — The unique ID of the tenant.
    
</dd>
</dl>

<dl>
<dd>

**take:** `typing.Optional[int]` — Maximum number of items to return per page. Defaults to 50. Maximum 50
    
</dd>
</dl>

<dl>
<dd>

**from:** `typing.Optional[str]` — Checkpoint cursor for pagination; use the 'next' value from a previous response to fetch the next page
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

