from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class Settings(BaseSettings):
    # Environment variables
    ENVIRONMENT: str = "development"
    SECRET_KEY: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
   
    # Generate asynchronous PostgreSQL DSN
    @property
    def POSTGRES_DSN(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                path=f"{self.POSTGRES_DB}",  # Ensure the path starts with a '/'
            )
        )

    class Config:
        env_file = None
        env_file_encoding = "utf-8"


# Instantiate the settings
settings = Settings()