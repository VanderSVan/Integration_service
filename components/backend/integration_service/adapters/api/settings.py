from pydantic import BaseSettings


class Settings(BaseSettings):
    API_TITLE: str = 'Validation API'
    API_VERSION: str = '1'
    API_PREFIX: str = f'/api/v{API_VERSION}'
    DOCS_URL: str = f'{API_PREFIX}/docs'
    REDOC_URL: str = f'{API_PREFIX}/redoc'
    OPENAPI_URL: str = f'{API_PREFIX}/openapi.json'

    LOGGING_LEVEL: str = 'DEBUG'
