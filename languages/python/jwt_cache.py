# Python JWT Cache and Authentication (`jwt_cache.py`)

[⬆ Back to Parent](../README.md)
[🏠 Back to Root README (../../../../README.md)

## Parent Context

This script is part of the Python language notes and utilities, specifically focusing on advanced JWT authentication and caching.

## Contents Overview

The `jwt_cache.py` module provides a robust and asynchronous mechanism for handling JWT token validation, JWKS caching, and user authentication within a Python application, likely using FastAPI. It includes logic for refreshing JWKS, decoding JWT payloads, retrieving user information from a database, and dynamically managing Row-Level Security (RLS) based on user's organization group claims embedded in the JWT.

## Role in System

This module is critical for securing APIs that rely on JWTs for authentication and authorization, especially in environments where token validation performance and dynamic access control are important. The caching mechanism reduces overhead by minimizing repeated JWKS fetches, while the RLS integration ensures granular data access based on user roles and groups.

## Key Components and Functions

### Global Caches

-   `jwks_cache`, `jwks_expiry`: Global variables to store and manage the expiration of the JSON Web Key Set.
-   `organisation_group_dict`: Cache for organization group data to optimize RLS lookups.

### `async def fetch_jwks()`

-   Asynchronously fetches the JWKS from the OIDC provider's endpoint.
-   Implements a caching mechanism (`jwks_cache`, `jwks_expiry`) to reduce external API calls.
-   Configured via `OIDC_BASE_URL` and `OIDC_REALM_NAME` environment variables.

### `async def get_token(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))) -> str`

-   FastAPI dependency to extract the Bearer token from the request.

### `async def find_rsa_key_in_jwks(jwks)`

-   Helper function to locate a suitable RSA public key within the fetched JWKS for token signature verification.

### `async def decode_payload(token: str, retry: bool = True) -> dict`

-   Decodes the JWT token using the fetched and cached JWKS.
-   Includes retry logic to refresh the JWKS cache if token validation fails due to an outdated key.
-   Handles various `JWTError` exceptions and other unexpected errors.

### `async def verify_key(payload: dict, key: str)`

-   Safely extracts a value from the JWT payload, raising an `HTTPException` if the key is missing or the payload is invalid.

### `async def get_db_user(db: AsyncSession, payload: dict)`

-   Retrieves a `User` object from the database based on `id_provider_username` and `email` from the JWT payload.
-   Ensures the user exists in the database and loads their associated roles.

### `async def get_user_organisation_group_ids(organisation_groups: [])`

-   Parses a list of organization group full paths from the JWT payload and matches them against cached database organization group paths to return corresponding IDs.

### `async def generate_user_organisation_group_access(db: AsyncSession, user_organisation_group_ids: str)`

-   Creates a `UserOrganisationGroupAccess` entry in the RLS database, associating the user with their identified organization groups.

### `async def save_user_organisation_group_access_log(db: AsyncSession, dashboard_id: int, user_dashboard_access_id: str)`

-   Logs user access to dashboards based on their organization group access.

### `async def get_user_dashboard_access_uuid(db: AsyncSession, user_id: int)`

-   Retrieves the most recent `UserOrganisationGroupAccess` UUID for a given user within a specified time frame.

### `async def populate_organisation_group_dict(db: AsyncSession)`

-   Populates the `organisation_group_dict` cache with external IDs and full paths of active organization groups from the database.

### `async def refresh_organisation_group_cache(db: AsyncSession)`

-   Triggers `populate_organisation_group_dict` if the organization group cache is outdated.

### `async def get_user_organisation_groups(current_user: User, dashboard_id: int, token: str = "") -> Optional[dict]`

-   Main function to extract user's organization groups from the JWT, process them, and store access information for RLS.

### `async def verify_user(db: AsyncSession, payload: dict = {})`

-   Verifies the user's identity and authorization based on audience (`CLIENT_ID`) and specific roles (`FRONTEND_CLIENT_ID`, `frontend_role`) within the JWT's `resource_access` claims.

### `async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(get_token)) -> Optional[User]`

-   The primary FastAPI dependency for obtaining the authenticated and authorized `User` object, including setting the `current_user_id` in the application context.

## Dependencies

-   `logging`, `os`, `requests`, `datetime`, `timedelta`
-   `jose` (`jwt`, `jwk`, `JWTError`)
-   `fastapi` (`Depends`, `HTTPException`, `status`)
-   `fastapi.security` (`OAuth2PasswordBearer`)
-   `sqlalchemy`, `sqlalchemy.orm`, `sqlalchemy.ext.asyncio`
-   `src.db` (`get_db`)
-   `src.utils.context` (`set_current_user_id`)
-   `src.model.rls` (`UserOrganisationGroupAccess`, `get_rls_db`)
-   `src.model` (`User`, `OrganisationGroup`, `UserOrganisationGroupAccessLog`)

## Environment Variables

-   `OIDC_BASE_URL`: Base URL of the OpenID Connect provider.
-   `OIDC_REALM_NAME`: Realm name for the OIDC provider.
-   `CLIENT_ID`: Expected audience/client ID for the application.
-   `FRONTEND_CLIENT_ID`: Client ID for the frontend application, used in role verification.