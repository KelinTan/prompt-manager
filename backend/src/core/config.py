import json
from enum import Enum
from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings


class AppEnv(str, Enum):
    dev = "dev"
    beta = "beta"
    prod = "prod"

    def is_not_prod(self):
        return self != AppEnv.prod

    def is_dev(self):
        return self == AppEnv.dev

    def is_prod(self):
        return self == AppEnv.prod


class EnvSettings(BaseSettings):
    openai_key: str = ""
    openai_model: str = ""
    db_host: str = "localhost"
    db_user: str = "root"
    db_password: str = "password"
    app_env: AppEnv = AppEnv.dev
    ali_dashscope_api_key: str = ""
    model_config = ConfigDict(env_file=".env")  # noqa


class LocalSettings(BaseModel):
    aigc_admins: list[str] | None = None

    @classmethod
    def from_yaml(cls, file_path: str, environment: str):
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
        if environment not in data:
            raise ValueError(f"Environment '{environment}' not found in {file_path}")
        return cls(**data[environment])


class Settings:
    def __init__(self):
        self.env = EnvSettings()
        local_config_file = str(Path(__file__).parent.parent.parent / "config.yaml")
        self.local = LocalSettings.from_yaml(local_config_file, self.env.app_env)
        print(f"Local settings loaded: {json.dumps(self.local.model_dump())}")

    def __getattr__(self, name):
        if hasattr(self.env, name):
            return getattr(self.env, name)
        if hasattr(self.local, name):
            return getattr(self.local, name)
        raise AttributeError(f"Configuration key '{name}' not found.")

    def dict(self):
        return {**self.env.model_dump(), **self.local.model_dump()}

    def model_dump(self):
        return self.dict()


settings = Settings()


@lru_cache
def get_settings():
    return settings
