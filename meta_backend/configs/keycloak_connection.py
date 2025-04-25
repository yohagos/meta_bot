from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.openapi.utils import get_openapi
from keycloak import KeycloakOpenID
from typing import Annotated, List
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

from .config import Settings, load_settings
from database import get_sync_session, lifespan, get_async_session

settings: Settings = load_settings() 

app = FastAPI(
    title="FastAPI Backend",
    description="API secured with OAuth2",
    version="1.0.0",
    swagger_ui_init_oauth={
        "clientId": settings.KEYCLOAK_CLIENT_ID,
        "clientSecret": settings.KEYCLOAK_CLIENT_SECRET,
        "appName": "FastAPI Backend",
        "usePkceWithAuthorizationCodeGrant": True
    },
    lifespan=lifespan
)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.AUTHORIZATION_URL,
    tokenUrl=settings.TOKEN_URL,
    scheme_name="OAuth2"
)

_keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_URL,
    realm_name=settings.KEYCLOAK_REALM,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
    verify=False
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes
    )
    openapi_schema["components"]["securitySchema"] = {
        "OAuth2": {
            "type": "oauth2",
            "flows": {
                "authorizationCode": {
                    "authorizationUrl": settings.AUTHORIZATION_URL,
                    "tokenUrl": settings.TOKEN_URL,
                    "scopes": {"openid": "openid"}
                }
            }
        }
    }
    openapi_schema["security"] = [{"OAuth2": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def configure_app():
    app.openapi = custom_openapi
    return app


def get_oauth_scheme():
    return oauth2_scheme

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No token provided"
        )
    try:
        decoded_token = _keycloak_openid.decode_token(
            token,
            key=_keycloak_openid.certs(),
            options={"verify_signature": False, "verify_aud": False}
        )
        roles = decoded_token.get("realm_access", {}).get("roles", [])
        decoded_token["roles"] = roles
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error occurred while decoding token"
        )
    
def check_roles(required_roles: List[str]):
    async def role_checker(user: dict = Depends(get_current_user)):
        user_roles = user.get("roles", [])

        if not any(role in required_roles for role in user_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return user
    return role_checker
    
SessionDep = Annotated[Session, Depends(get_sync_session)]
AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
