import logging
from fastapi import Depends
from keycloak import KeycloakAdmin
from uuid import UUID

from . import Settings, load_settings
from models import user
from utils import logger

settings: Settings = load_settings()

class KeycloakUserService: 
    def __init__(self, kc_admin: KeycloakAdmin):
        self.kc_admin = kc_admin
    
    def get_user_info(self, user_id: UUID) -> user.User | None:
        try: 
            raw_user = self.kc_admin.get_user(str(user_id))
            return user.User(
                firstName=raw_user.get("firstName", ""),
                lastName=raw_user.get("lastName", ""),
                email=raw_user.get("email", "")
            )
        except Exception as e:
            logger.error(f"Keycloak ERROR : {str(e)}")
            return None

def get_keycloak_admin() -> KeycloakAdmin:
    return KeycloakAdmin(
        server_url=settings.KEYCLOAK_URL,
        realm_name=settings.KEYCLOAK_REALM,
        client_id=settings.KEYCLOAK_CLIENT_ID,
        client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
        verify=False
    )

def get_keycloak_service(kc_admin: KeycloakAdmin = Depends(get_keycloak_admin)) -> KeycloakUserService:
    return KeycloakUserService(kc_admin)