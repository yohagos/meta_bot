import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    DB_USER: str  = os.getenv('DB_USER')
    DB_PASSWORD: str  = os.getenv('DB_PASSWORD')
    DB_URL: str  = os.getenv('DB_URL')
    DB_NAME: str  = os.getenv('DB_NAME')

    KEYCLOAK_URL: str = os.getenv('KEYCLOAK_URL')
    KEYCLOAK_REALM: str = os.getenv('KEYCLOAK_REALM')
    KEYCLOAK_CLIENT_ID: str = os.getenv('KEYCLOAK_CLIENT_ID')
    KEYCLOAK_CLIENT_SECRET: str = os.getenv('KEYCLOAK_CLIENT_SECRET')
    CALLBACK_URI: str = os.getenv('CALLBACK_URI')

    AUTHORIZATION_URL: str = os.getenv('AUTHORIZATION_URL')
    TOKEN_URL: str = os.getenv('TOKEN_URL')

    COIN_URL: str = os.getenv('COIN_URL')

    MQ_USER: str = os.getenv('MQ_USER')
    MQ_PASSWORD: str = os.getenv('MQ_PASSWORD')
    MQ_VHOST: str = os.getenv('MQ_VHOST', '/meta')
    MQ_EXCHANGE: str = os.getenv('MQ_EXCHANGE')
    MQ_QUEUE: str = os.getenv('MQ_QUEUE')
    MQ_ROUTING_KEY: str = os.getenv('MQ_ROUTING_KEY')

    MODE: str = os.getenv('MODE')


def load_settings() -> Settings:
    return Settings()
