from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_name: str = "gpt-4o-mini"
    openai_api_key: str | None = None
    github_token: str | None = None
    github_owner: str | None = None
    github_repo: str | None = None
    a2a_coding_agent_url: str | None = None
    project_tool: str = "github_projects"
    require_human_approval: bool = True

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
