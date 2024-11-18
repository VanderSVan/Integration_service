from pathlib import Path

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    API_URL: str = Field(..., env='YANDEXGPT_API_URL')
    FOLDER_ID: str = Field(..., env='FOLDER_ID')
    IAM_TOKEN: str = Field(..., env='IAM_TOKEN')

    class Config:
        env_file = Path(__file__).parent.parent.parent.parent.parent.joinpath(".env")
        env_file_encoding = 'utf-8'
