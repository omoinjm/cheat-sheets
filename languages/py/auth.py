# OAuth example for python

import logging
import os
import requests
from jose import jwt, jwk, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from src.db import get_db
from src.model import (
    User,
    Provider,
    ProviderVersion,
    ProviderAuthenticationType,
)


cache_dict = {}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
four_oh_three = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Authentication Failed"
)


def get_token(token: str = Depends(oauth2_scheme)) -> str:
    return token


def decode_payload(token: str) -> dict:
    # JOSE library does not support the dynamic keys used by Keycloak natively,
    # so we fetch the JSON Web Key Set (JWKS) from the discovery endpoint and convert it to a PEM key:
    base_url = os.getenv("OIDC_BASE_URL")
    realm_name = os.getenv("OIDC_REALM_NAME")
    issuer_url = f"{base_url}/realms/{realm_name}"
    cert_url = f"{issuer_url}/protocol/openid-connect/certs"
    try:
        jwks_request = requests.get(cert_url, timeout=2.0)
        jwks = jwks_request.json()
        rsa_key = None
        for key in jwks.get('keys', []):
            if key.get('kty', None) == 'RSA' and key.get('use', None) == 'sig':
                rsa_key = key
                break
        if not rsa_key:
            raise JWTError('No suitable key found in JWKS.')
        # Constructing RSA key from JWKS:
        key = jwk.construct(rsa_key)
        # Decoding our token:
        payload = jwt.decode(token, key, algorithms=["RS256"], options={"verify_aud": False})
    except JWTError as e:
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
            detail=f"Invalid request - {str(e)}"
        )
    return payload


# Parses semi-colon separated list of providers each corresponding
# to a JSON object named {provider_name}: {provider_setup_info}
def get_parsed_payload_providers(payload: dict = {}):
    payload_providers = payload.get('providers', ';')
    split_payload_providers = payload_providers.split(';')
    parsed_payload_providers = {name: payload.get(name) for name in split_payload_providers}
    return parsed_payload_providers


def verify_key(payload: dict, key: str):
    value = payload.get(key, None)
    if value:
        return value
    raise four_oh_three


def create_provider_authentication_type_if_not_exists(
    db: Session,
    name: str
) -> ProviderAuthenticationType:
    provider_authentication_type = db.query(ProviderAuthenticationType). \
        filter(ProviderAuthenticationType.name == name). \
        filter(ProviderAuthenticationType.deleted.is_(False)). \
        first()
    if not provider_authentication_type:
        provider_authentication_type = ProviderAuthenticationType(name=name)
        db.add(provider_authentication_type)
        db.flush()
        db.refresh(provider_authentication_type)
    return provider_authentication_type


def create_provider_if_not_exists(db: Session, provider_name: str) -> Provider:
    provider = db.query(Provider). \
        filter(Provider.name == provider_name.lower()). \
        filter(Provider.deleted.is_(False)). \
        first()
    if not provider:
        provider = Provider(name=provider_name)
        db.add(provider)
        db.flush()
        db.refresh(provider)
    return provider


def create_provider_version_if_not_exists(
        db: Session,
        provider: Provider,
        provider_data: dict = {},
):
    provider_authentication_type_name = provider_data.pop('provider_authentication_type')
    provider_authentication_type = create_provider_authentication_type_if_not_exists(
        db=db,
        name=provider_authentication_type_name
    )
    provider_data['auth_type_id'] = provider_authentication_type.id

    provider_version = db.query(ProviderVersion). \
        filter(ProviderVersion.deleted.is_(False))
    for key, value in provider_data.items():
        if not hasattr(provider_version, key):
            continue
        pv_attr = getattr(ProviderVersion, key)
        provider_version = provider_version.filter(pv_attr == value)
    provider_version = provider_version.first()
    if not provider_version:
        provider_version = ProviderVersion(**provider_data)
        db.add(provider_version)
        db.flush()
        db.refresh(provider_version)
    provider.versions.append(provider_version)
    db.add(provider)
    db.flush()
    db.refresh(provider)
    return provider_version


def ensure_providers(db: Session, parsed_payload_providers: dict = {}) -> bool:
    for provider_name, provider_config in parsed_payload_providers.items():
        provider = create_provider_if_not_exists(
            db=db,
            provider_name=provider_name
        )
        provider_version = create_provider_version_if_not_exists(
            db=db,
            provider=provider,
            provider_data=provider_config,
        )
        if not provider_version:
            return False
    return True


def get_db_user(
        db: Session,
        payload: dict
):
    user_dict = {
        'name': verify_key(payload=payload, key='preferred_username'),
        'id_provider_username': verify_key(payload=payload, key='sub'),
        'email': verify_key(payload=payload, key='email'),
    }
    user = db.query(User). \
        filter(User.id_provider_username == user_dict.get('id_provider_username')). \
        filter(User.email == user_dict.get('email')). \
        first()
    if not user:
        user = User(**user_dict)
        db.add(user)
        db.flush()
        db.commit()
        db.refresh(user)
    return user


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(get_token)
) -> Optional[User]:

    payload = decode_payload(token=token)

    user = get_db_user(db=db, payload=payload)
    audience = verify_key(payload=payload, key='aud')
    resource_provider_client_id = os.getenv("CLIENT_ID", "ImprobableThatThisIsAClientID4OurApps")
    if resource_provider_client_id not in audience:
        raise four_oh_three

    parsed_payload_providers = get_parsed_payload_providers(payload=payload)
    providers_ensured = ensure_providers(db=db, parsed_payload_providers=parsed_payload_providers)
    if not providers_ensured:
        return False
    return user
