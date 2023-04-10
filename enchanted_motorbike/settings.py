from pydantic import BaseSettings, Field


class _Controller(BaseSettings):
    host: str = Field("controller")
    port: int = Field(8000)
    decision_interval_seconds: float = Field(5.0)

    @property
    def full_hostname(self) -> str:
        return f"http://{self.host}:{self.port}"


class _Manipulator(BaseSettings):
    host: str = Field("manipulator")
    port: int = Field(8000)

    @property
    def address(self) -> tuple[str, int]:
        return self.host, self.port


class _Redis(BaseSettings):
    host: str = Field(env="REDIS_HOST")
    password: str = Field(env="REDIS_PASSWORD")
    port: int = Field(6379)

    class Config:
        env_file = ".env"


class _Settings(BaseSettings):
    controller = _Controller()
    manipulator = _Manipulator()
    redis = _Redis()


settings = _Settings()
