from pydantic import BaseSettings


class DBSettings(BaseSettings):
    fake: bool = False
    host: str = "localhost"
    port: int = 5432
    user: str
    password: str
    database: str
    driver: str = "postgresql"

    @property
    def url(self) -> str:
        return (
            f"{self.driver}://{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.database}"
        )

    class Config:
        env_prefix = "DB_"


class Settings(BaseSettings):
    debug: bool = True
    title: str = "fastapi-registration"

    page_size: int = 40

    db: DBSettings = DBSettings()


settings = Settings()
