from functools import lru_cache

import pydantic


class ServerSettings(pydantic.BaseSettings):
    database_url: str = "sqlite+aiosqlite:///fastgql.db"

    class Config:
        env_prefix = "fastgql_"
        env_file = ".env"
        env_file_encoding = "utf-8"

    def __hash__(self) -> int:
        return hash(self.json())


@lru_cache
def get_server_settings() -> ServerSettings:
    return ServerSettings()
