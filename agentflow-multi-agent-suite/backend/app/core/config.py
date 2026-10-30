from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator
from typing import List, Union


class Settings(BaseSettings):
    APP_NAME: str = "AgentFlow Multi-Agent Suite"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "change-me"

    BACKEND_CORS_ORIGINS: List[Union[str, AnyHttpUrl]] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    DATABASE_URL: str = "sqlite+aiosqlite:///./agentflow.db"

    OPENROUTER_API_KEY: str = ""
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_SITE_URL: str = "http://localhost:5173"
    OPENROUTER_APP_NAME: str = "AgentFlow"

    BROWSER_HEADLESS: bool = False
    BROWSER_VIEWPORT_WIDTH: int = 1280
    BROWSER_VIEWPORT_HEIGHT: int = 720
    CDP_SCREENCAST_QUALITY: int = 70
    CDP_SCREENCAST_MAX_FPS: int = 12

    AUTO_TAKEOVER_ON_POST_LOGIN: bool = True
    PAUSE_ON_CAPTCHA: bool = True
    CONFIRM_BEFORE_SUBMIT: bool = True
    MAX_AGENT_REVISIONS: int = 3
    APPROVAL_THRESHOLD: int = 70

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
