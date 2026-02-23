# Python OAuth Authentication Example (`auth.py`)

[⬆ Back to Parent](../README.md)
[🏠 Back to Root README (../../../../README.md)

## Parent Context

This script is part of the Python language notes and utilities, specifically focusing on authentication mechanisms.

## Contents Overview

The `auth.py` module provides an OAuth 2.0 implementation for Python applications, likely intended for use with frameworks like FastAPI. It integrates with an OpenID Connect (OIDC) provider (e.g., Keycloak) to decode and validate JSON Web Tokens (JWTs). Key functionalities include fetching JSON Web Key Sets (JWKS) to verify token signatures, extracting payload information, and managing associated database models (`User`, `Provider`, `ProviderVersion`, `ProviderAuthenticationType`).

## Role in System

This module is crucial for securing API endpoints by implementing robust authentication and authorization checks. It abstracts the complexities of OAuth 2.0 and OIDC token validation, ensuring that only authenticated and authorized users can access protected resources. It also handles the dynamic registration of authentication providers and their versions within the application's database.

## Key Components and Functions

### `get_token(token: str = Depends(oauth2_scheme)) -> str`

-   A FastAPI dependency that extracts the Bearer token from the request header.

### `decode_payload(token: str) -> dict`

-   Decodes a given JWT token.
-   Fetches the JSON Web Key Set (JWKS) from the OIDC provider's discovery endpoint (configured via `OIDC_BASE_URL` and `OIDC_REALM_NAME` environment variables).
-   Converts the appropriate RSA key from the JWKS into a PEM key for token verification.
-   Raises `HTTPException` for invalid tokens, unauthorized access, or other errors during decoding.

### `get_parsed_payload_providers(payload: dict = {})`

-   Parses a semi-colon separated string of providers from the JWT payload into a dictionary, where each provider corresponds to a JSON object.

### `verify_key(payload: dict, key: str)`

-   A utility function to safely retrieve a key's value from the payload, raising a `403 HTTPException` if the key is missing.

### Database Interaction Functions

-   `create_provider_authentication_type_if_not_exists(db: Session, name: str) -> ProviderAuthenticationType`
-   `create_provider_if_not_exists(db: Session, provider_name: str) -> Provider`
-   `create_provider_version_if_not_exists(db: Session, provider: Provider, provider_data: dict = {})`
    -   These functions ensure that `ProviderAuthenticationType`, `Provider`, and `ProviderVersion` records exist in the database, creating them if necessary. They manage the relationship between providers and their versions based on data extracted from the JWT.

### `ensure_providers(db: Session, parsed_payload_providers: dict = {}) -> bool`

-   Iterates through the parsed providers from the JWT payload and ensures their existence in the database, creating associated records as needed.

### `get_db_user(db: Session, payload: dict)`

-   Retrieves or creates a `User` record in the database based on information (`preferred_username`, `sub`, `email`) extracted from the JWT payload.

### `get_current_user(db: Session = Depends(get_db), token: str = Depends(get_token)) -> Optional[User]`

-   The main dependency for obtaining the currently authenticated user.
-   Decodes the token, verifies the audience (`aud`) against a `CLIENT_ID` environment variable, ensures all providers referenced in the token are present in the database, and returns the `User` object.
-   Raises `HTTPException` for various authentication failures.

## Dependencies

-   `logging`, `os`, `requests`
-   `jose` (for JWT operations)
-   `fastapi` (`Depends`, `HTTPException`, `status`)
-   `fastapi.security` (`OAuth2PasswordBearer`)
-   `sqlalchemy.orm` (`Session`)
-   `src.db` (`get_db`)
-   `src.model` (`User`, `Provider`, `ProviderVersion`, `ProviderAuthenticationType`)

## Environment Variables

-   `OIDC_BASE_URL`: Base URL of the OpenID Connect provider.
-   `OIDC_REALM_NAME`: Realm name for the OIDC provider.
-   `CLIENT_ID`: Expected audience/client ID for the application.