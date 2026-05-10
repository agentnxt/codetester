from functools import lru_cache
from pydantic import Field, AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore', case_sensitive=False)

    app_name: str = 'GitHub Deployment Orchestrator Assistant'
    environment: str = 'development'
    model_name: str = 'gpt-4o-mini'
    openai_api_key: str | None = None

    github_token: str | None = None
    github_owner: str | None = None
    github_repo: str | None = None
    github_app_id: str | None = None
    github_app_private_key: str | None = None
    github_webhook_secret: str | None = None

    a2a_coding_agent_url: str | None = None
    project_tool: str = 'github_projects'
    require_human_approval: bool = True

    database_url: str = 'sqlite:///./orchestrator.db'
    redis_url: str = 'redis://localhost:6379/0'
    cors_origins: str = 'http://localhost:3000'
    api_key: str | None = Field(default=None, description='Optional API key for UI/API access')

    log_level: str = 'INFO'

    @property
    def cors_origin_list(self) -> list[str]:
        return [x.strip() for x in self.cors_origins.split(',') if x.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
