from pydantic_settings import BaseSettings, SettingsConfigDict

POSTGRE_SQL = "postgresql+asyncpg://myuser:mypassword@localhost/mydb"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        )

    DATABASE_URL: str = POSTGRE_SQL
    SECRET_KEY: str = "CHANGE_ME_TO_SECURE"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

settings = Settings()
