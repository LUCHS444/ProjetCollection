from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    cors_origin: str = "http://localhost:5173"

    class Config:
        env_file = ".env"


settings = Settings()