from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str = "sqlite:///./finance.db"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
