# Auth0 Teams SDK for Python

<div align="center">

[![pypi](https://img.shields.io/pypi/v/auth0-teams-python)](https://pypi.python.org/pypi/auth0-teams-python)
[![License](https://img.shields.io/:license-Apache%202.0-blue.svg?style=flat)](https://github.com/auth0/teams-python/blob/HEAD/LICENSE)
[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-Built%20with%20Fern-brightgreen)](https://buildwithfern.com?utm_source=github&utm_medium=github&utm_campaign=readme&utm_source=https%3A%2F%2Fgithub.com%2Fauth0%2Fteams-python)

🚀 [Installation](#installation) • 📖 [Reference](#reference) • 💬 [Feedback](#feedback)

</div>

---

The Auth0 Teams SDK for Python provides convenient access to the Auth0 Teams API from Python.

## Installation

```sh
pip install auth0-teams-python
```

**Requirements:**
- Python ≥3.10

## Reference

A full reference for this library is available [here](https://github.com/auth0/teams-python/blob/HEAD/./reference.md).

## Usage

The client supports two authentication modes. With an existing token (a static string,
or a callable that returns one from your own auth flow):

```python
from auth0.teams import Teams

client = Teams(
    team_slug="acme",
    tenant_domain="acme.us.auth0.com",
    token="<token>",
)
```

For backend scripts or admin tooling, pass client credentials and the SDK acquires and
refreshes the token for you via the OAuth 2.0 client credentials grant:

```python
from auth0.teams import Teams

client = Teams(
    team_slug="acme",
    tenant_domain="acme.us.auth0.com",
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
)
```

Then call the API:

```python
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

The API base URL and audience are derived from `team_slug`
(`https://{team_slug}.teams.auth0.com`). Override either with the `base_url` or
`audience` parameters when needed.

## Async Client

The SDK also exports an `async` client so that you can make non-blocking calls to our API. Note that if you are constructing an Async httpx client class to pass into this client, use `httpx.AsyncClient()` instead of `httpx.Client()` (e.g. for the `httpx_client` parameter of this client).

```python
import asyncio

from auth0.teams import AsyncTeams

client = AsyncTeams(
    team_slug="acme",
    tenant_domain="acme.us.auth0.com",
    token="<token>",
)


async def main() -> None:
    await client.members.invite(
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


asyncio.run(main())
```

## Exception Handling

When the API returns a non-success status code (4xx or 5xx response), a subclass of the following error
will be thrown.

```python
from auth0.teams.core.api_error import ApiError

try:
    client.members.invite(...)
except ApiError as e:
    print(e.status_code)
    print(e.body)
```

## Pagination

Paginated requests will return a `SyncPager` or `AsyncPager`, which can be used as generators for the underlying object.

```python
from auth0.teams import Teams

client = Teams(
    team_slug="acme",
    tenant_domain="acme.us.auth0.com",
    token="<token>",
)

client.members.list(
    take=1,
    from_="from",
)
```

```python
# You can also iterate through pages and access the typed response per page
pager = client.members.list(...)
for page in pager.iter_pages():
    print(page.response)  # access the typed response for each page
    for item in page:
        print(item)
```

## Advanced

### Access Raw Response Data

The SDK provides access to raw response data, including headers, through the `.with_raw_response` property.
The `.with_raw_response` property returns a "raw" client that can be used to access the `.headers` and `.data` attributes.

```python
from auth0.teams import Teams

client = Teams(...)
response = client.members.with_raw_response.invite(...)
print(response.headers)  # access the response headers
print(response.status_code)  # access the response status code
print(response.data)  # access the underlying object
```

### Retries

The SDK is instrumented with automatic retries with exponential backoff. A request will be retried as long
as the request is deemed retryable and the number of retry attempts has not grown larger than the configured
retry limit (default: 2).

A request is deemed retryable when any of the following HTTP status codes is returned:

- [408](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/408) (Timeout)
- [429](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) (Too Many Requests)
- [5XX](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500) (Internal Server Errors)

Use the `max_retries` request option to configure this behavior.

```python
client.members.invite(..., request_options={
    "max_retries": 1
})
```

### Timeouts

The SDK defaults to a 60 second timeout. You can configure this with a timeout option at the client or request level.

```python
from auth0.teams import Teams

client = Teams(..., timeout=20.0)

# Override timeout for a specific method
client.members.invite(..., request_options={
    "timeout_in_seconds": 1
})
```

### Additional Headers

If you would like to send additional headers as part of the request, use the `headers` parameter:

```python
from auth0.teams import Teams

client = Teams(
    team_slug="acme",
    tenant_domain="acme.us.auth0.com",
    token="<token>",
    headers={"X-Custom-Header": "custom value"},
)
```

### Logging

The SDK includes built-in logging that can help with debugging. You can enable it by passing a `logging` configuration when creating the client:

```python
from auth0.teams import Teams

client = Teams(
    team_slug="acme",
    tenant_domain="acme.us.auth0.com",
    token="<token>",
    logging={"level": "debug"},
)
```

When enabled at `debug` level, the SDK logs HTTP request and response details including method, URL, status code, and headers. Sensitive information (authorization headers, API keys) is automatically redacted.

### Telemetry

The SDK sends an `Auth0-Client` header identifying the SDK name, version, and Python
runtime. If you are building an SDK or tool on top of this client, override that header
with your own attribution using `client_info`:

```python
from auth0.teams import Teams

client = Teams(
    team_slug="acme",
    tenant_domain="acme.us.auth0.com",
    token="<token>",
    client_info={"name": "my-wrapper", "version": "1.0.0"},
)
```

### Custom Client

You can override the `httpx` client to customize it for your use-case. Some common use-cases include support for proxies
and transports.

```python
import httpx
from auth0.teams import Teams

client = Teams(
    ...,
    httpx_client=httpx.Client(
        proxy="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

## Feedback

### Contributing

We appreciate feedback and contribution to this repo! Before you get started, please see the following:

- [Auth0's general contribution guidelines](https://github.com/auth0/open-source-template/blob/master/GENERAL-CONTRIBUTING.md)
- [Auth0's code of conduct guidelines](https://github.com/auth0/open-source-template/blob/master/CODE-OF-CONDUCT.md)

While we value open-source contributions to this SDK, this library is generated programmatically.
Additions made directly to this library would have to be moved over to our generation code,
otherwise they would be overwritten upon the next generated release. Feel free to open a PR as
a proof of concept, but know that we will not be able to merge it as-is. We suggest opening
an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!

### Raise an issue

To provide feedback or report a bug, please [raise an issue on our issue tracker](https://github.com/auth0/teams-python/issues).

### Vulnerability Reporting

Please do not report security vulnerabilities on the public GitHub issue tracker. The [Responsible Disclosure Program](https://auth0.com/responsible-disclosure-policy) details the procedure for disclosing security issues.

## What is Auth0?

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://cdn.auth0.com/website/sdks/logos/auth0_dark_mode.png" width="150">
    <source media="(prefers-color-scheme: light)" srcset="https://cdn.auth0.com/website/sdks/logos/auth0_light_mode.png" width="150">
    <img alt="Auth0 Logo" src="https://cdn.auth0.com/website/sdks/logos/auth0_light_mode.png" width="150">
  </picture>
</p>
<p align="center">
  Auth0 is an easy to implement, adaptable authentication and authorization platform. To learn more checkout <a href="https://auth0.com/why-auth0">Why Auth0?</a>
</p>
<p align="center">
  Copyright 2026 Okta, Inc. This project is licensed under the <a href="./LICENSE">Apache License 2.0</a>. See the <a href="./LICENSE">LICENSE</a> file for details.
</p>
