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


class _Mongo(BaseSettings):
    host: str = Field(env="MONGO_HOST")
    username: str = Field(env="MONGO_USERNAME")
    password: str = Field(env="MONGO_PASSWORD")
    port: int = Field(27017)

    @property
    def url(self) -> str:
        credentials = f"{self.username}:{self.password}"
        address = f"{self.host}:{self.port}"
        return f"mongodb://{credentials}@{address}"

    class Config:
        env_file = ".env"


class _Settings(BaseSettings):
    controller = _Controller()
    manipulator = _Manipulator()
    mongo = _Mongo()


settings = _Settings()
