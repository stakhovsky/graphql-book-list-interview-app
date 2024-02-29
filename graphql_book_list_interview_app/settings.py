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

    def _build_dsn(
        self,
        proto: str = "postgresql",
    ) -> str:
        return f"{proto}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

    @property
    def db_dsn(self) -> str:
        return self._build_dsn(
            proto="postgresql+asyncpg",
        )

    @property
    def migration_db_dsn(self):
        return self._build_dsn(
            proto="postgresql+psycopg",
        )
