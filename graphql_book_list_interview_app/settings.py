from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    user: str
    password: str
    host: str
    port: int
    db: str

    model_config = SettingsConfigDict(
        env_prefix='POSTGRES_'
    )

    @property
    def db_dsn(self) -> str:
        proto = "postgresql+asyncpg"
        return f"{proto}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
