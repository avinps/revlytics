from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    review_stream_rate: int = 2

    class Config:
        env_file = ".env"

settings = Settings()