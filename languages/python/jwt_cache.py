import logging
import os
import requests
from datetime import datetime, timedelta
from jose import jwt, jwk, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from src.db import get_db
from src.utils.context import set_current_user_id
from src.model.rls import UserOrganisationGroupAccess, get_rls_db
from src.model import User, OrganisationGroup, UserOrganisationGroupAccessLog


# Initialize cache and expiry
jwks_cache = None
jwks_expiry = None
organisation_group_dict = {"timestamp": datetime.now() - timedelta(minutes=31)}


async def fetch_jwks():
    global jwks_cache, jwks_expiry
    # Check if JWKS is expired
    base_url = os.getenv("OIDC_BASE_URL")
    realm_name = os.getenv("OIDC_REALM_NAME")
    issuer_url = f"{base_url}/realms/{realm_name}"
    cert_url = f"{issuer_url}/protocol/openid-connect/certs"
    if jwks_expiry and datetime.utcnow() < jwks_expiry:
        return jwks_cache
    try:
        jwks_request = requests.get(cert_url, timeout=5.0)
        jwks_cache = jwks_request.json()
        jwks_expiry = datetime.utcnow() + timedelta(minutes=15)  # Cache for 15 minutes
        return jwks_cache
    except requests.RequestException as e:
        logging.error(f"Could not fetch JWKS: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not fetch JWKS",
        )


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
four_oh_three = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Authentication Failed"
)


async def get_token(token: str = Depends(oauth2_scheme)) -> str:
    return token


async def find_rsa_key_in_jwks(jwks):
    for key in jwks.get("keys", []):
        if key.get("kty", None) == "RSA" and key.get("use", None) == "sig":
            return key
    raise JWTError("No suitable key found in JWKS.")


async def decode_payload(token: str, retry: bool = True) -> dict:
    global jwks_cache, jwks_expiry  # these are defined globally
    try:
        jwks = (
            await fetch_jwks()
        )  # fetch_jwks checks the cache and fetches new JWKS if needed
        rsa_key = await find_rsa_key_in_jwks(jwks)  # helper function to find RSA key
        key = jwk.construct(rsa_key)
        payload = jwt.decode(
            token, key, algorithms=["RS256"], options={"verify_aud": False}
        )
    except JWTError as e:
        if "Unable to find an algorithm for key" in str(e):
            # Add new handling for this specific JWTError
            # Example: Log and raise a different HTTPException or handle it differently
            logging.error(f"JWTError due to algorithm issue: {str(e)}")
        if retry:
            logging.warning("JWTError occurred; refreshing JWKS and retrying.")
            jwks_cache = None  # Invalidate the cache
            jwks_expiry = None
            return await decode_payload(token, retry=False)
        logging.error(f"Could not validate credentials: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid request - {str(e)}",
        )
    return payload


async def verify_key(payload: dict, key: str):
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid payload"
        )
    value = payload.get(key)
    if value:
        return value
    raise four_oh_three


async def get_db_user(db: AsyncSession, payload: dict):
    user_dict = {
        "name": await verify_key(payload=payload, key="preferred_username"),
        "id_provider_username": await verify_key(payload=payload, key="sub"),
        "email": await verify_key(payload=payload, key="email"),
    }
    if "sub" not in payload or "email" not in payload:
        logging.error("Missing required keys in payload")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing required payload keys",
        )
    query = (
        select(User)
        .options(selectinload(User.roles))
        .where(
            User.deleted_at.is_(None),
            User.id_provider_username == user_dict.get("id_provider_username"),
            User.email == user_dict.get("email"),
        )
    )
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User must exist in the database to make requests",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_user_organisation_group_ids(organisation_groups: []):
    db_organisation_group_full_paths = organisation_group_dict.get("full_paths", [])
    db_organisation_group_ids = organisation_group_dict.get("org_group_ids", [])
    matched_ids = []

    for organisation_group in organisation_groups:
        # We ensure the @ is replaced with / to avoid lookup errors
        organisation_group = organisation_group.replace("@", "/")
        if organisation_group not in db_organisation_group_full_paths:
            continue
        # Establish the top index of the first record where the full organisation group exists
        top_index = db_organisation_group_full_paths.index(organisation_group)
        end_index = None
        # Establish the bottom index of the first record containing the full path searching in reverse
        for db_org_group_fp in db_organisation_group_full_paths[::-1]:
            if db_org_group_fp.startswith(organisation_group):
                break
        end_index = db_organisation_group_full_paths.index(db_org_group_fp)
        for target_id in range(top_index, end_index + 1):
            target_org_full_path = str(db_organisation_group_ids[target_id])
            matched_ids.append(target_org_full_path)
    return matched_ids


async def generate_user_organisation_group_access(
    db: AsyncSession,
    user_organisation_group_ids: str,
):
    user_organisation_group_access = UserOrganisationGroupAccess(
        organisation_group_ids=user_organisation_group_ids,
    )
    db.add(user_organisation_group_access)
    await db.flush()
    await db.refresh(user_organisation_group_access)
    return user_organisation_group_access


async def save_user_organisation_group_access_log(
    db: AsyncSession,
    dashboard_id: int,
    user_dashboard_access_id: str,
):
    logging.warning(dashboard_id)
    logging.warning(user_dashboard_access_id)
    user_organisation_group_access_log = UserOrganisationGroupAccessLog(
        user_dashboard_access_id=user_dashboard_access_id,
        dashboard_id=dashboard_id,
    )
    db.add(user_organisation_group_access_log)
    await db.commit()


async def get_user_dashboard_access_uuid(
    db: AsyncSession,
    user_id: int,
):
    expire_time = datetime.now() - timedelta(minutes=10)
    query = (
        select(UserOrganisationGroupAccess)
        .where(
            UserOrganisationGroupAccess.created_by_id == user_id,
            UserOrganisationGroupAccess.created_at >= expire_time,
        )
        .order_by(UserOrganisationGroupAccess.created_at.desc())
        .limit(1)
    )
    result = await db.execute(query)
    uuid_query = result.scalar_one_or_none()
    return uuid_query


async def populate_organisation_group_dict(db: AsyncSession):
    query = (
        select(OrganisationGroup.external_id, OrganisationGroup.full_path)
        .where(OrganisationGroup.deleted_at.is_(None))
        .order_by(OrganisationGroup.full_path.asc())
    )
    result = await db.execute(query)
    organisation_group_query = result.all()
    if not organisation_group_query:
        return False
    organisation_group_dict["org_group_ids"] = [o[0] for o in organisation_group_query]
    organisation_group_dict["full_paths"] = [o[1] for o in organisation_group_query]
    organisation_group_dict["timestamp"] = datetime.now()
    return True


async def refresh_organisation_group_cache(db: AsyncSession):
    last_updated = organisation_group_dict.get("timestamp")
    expire_time = datetime.now() - timedelta(minutes=30)
    if isinstance(last_updated, datetime) and expire_time > last_updated:
        await populate_organisation_group_dict(db=db)
    return True


async def get_user_organisation_groups(
    current_user: User,
    dashboard_id: int,
    token: str = "",
) -> Optional[dict]:
    db_gen = get_db()
    async for db in db_gen:  # Iterate over the generator to get the db session
        await refresh_organisation_group_cache(db=db)

    payload = await decode_payload(token=token, retry=True)
    if not payload:
        return {"user": None, "user_dashboard_access": None}
    organisation_groups = payload.get("organisation_groups", [])
    prefix = "/organisation-groups/lytx/"
    organisation_groups = [
        group[len(prefix) :].replace("/", "\\")
        for group in organisation_groups
        if group.startswith(prefix)
    ]
    user_organisation_group_ids = await get_user_organisation_group_ids(
        organisation_groups
    )
    rls_db_gen = get_rls_db()
    async for rlsdb in rls_db_gen:  # Iterate over the generator to get the db session
        user_organisation_group_access = await generate_user_organisation_group_access(
            db=rlsdb,
            user_organisation_group_ids=user_organisation_group_ids,
        )
    async for db in get_db():
        await save_user_organisation_group_access_log(
            db=db,
            dashboard_id=dashboard_id,
            user_dashboard_access_id=getattr(user_organisation_group_access, "uuid"),
        )
    return user_organisation_group_access


async def verify_user(
    db: AsyncSession,
    payload: dict = {},
):
    user = await get_db_user(db=db, payload=payload)
    audience = await verify_key(payload=payload, key="aud")
    resource_provider_client_id = os.getenv(
        "CLIENT_ID", "ImprobableThatThisIsAClientID4OurApps"
    )
    if resource_provider_client_id not in audience:
        raise four_oh_three
    resource_access_dict = payload.get("resource_access", {})
    frontend_client_id = os.getenv("FRONTEND_CLIENT_ID")
    frontend_role = f"{frontend_client_id}-role"

    frontend_client_dict = resource_access_dict.get(frontend_client_id, None)
    if not frontend_client_dict:
        logging.warn(
            "Failed to get frontend_client_dict, FRONTEND_CLIENT_ID probably not set"
        )
        raise four_oh_three
    if frontend_role not in frontend_client_dict.get("roles", []):
        logging.warn("Failed to find frontend_role in frontend_client_dict[roles]")
        raise four_oh_three
    return user


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(get_token),
) -> Optional[User]:
    payload = await decode_payload(token=token, retry=True)
    user = await verify_user(db=db, payload=payload)
    if not user:
        raise four_oh_three
    await set_current_user_id(user_id=user.id)
    return user

