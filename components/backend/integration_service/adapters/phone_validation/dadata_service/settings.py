from pathlib import Path

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    API_URL: str = Field(..., env='DADATA_PHONE_API_URL')
    API_KEY: str = Field(..., env='DADATA_API_KEY')
    SECRET_KEY: str = Field(..., env='DADATA_SECRET_KEY')

    class Config:
        env_file = Path(__file__).parent.parent.parent.parent.parent.joinpath(".env")
        env_file_encoding = 'utf-8'
