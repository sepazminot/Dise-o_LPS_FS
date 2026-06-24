"""
Application configuration using pydantic-settings.
"""
from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )
    
    # Environment
    ENVIRONMENT: str = Field(default="development", description="Environment: development, staging, production")
    DEBUG: bool = Field(default=True, description="Debug mode")
    
    # HTTP Server
    HTTP_HOST: str = Field(default="0.0.0.0")
    HTTP_PORT: int = Field(default=8000)
    
    # gRPC Server
    GRPC_HOST: str = Field(default="0.0.0.0")
    GRPC_PORT: int = Field(default=50051)
    
    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://edu_user:edu_pass@localhost:5432/educational",
        description="Async PostgreSQL connection URL"
    )
    DATABASE_POOL_SIZE: int = Field(default=10)
    DATABASE_MAX_OVERFLOW: int = Field(default=20)
    DATABASE_POOL_TIMEOUT: int = Field(default=30)
    DATABASE_POOL_RECYCLE: int = Field(default=3600)
    
    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    REDIS_MAX_CONNECTIONS: int = Field(default=50)
    REDIS_SOCKET_TIMEOUT: int = Field(default=5)
    REDIS_SOCKET_CONNECT_TIMEOUT: int = Field(default=5)
    
    # JWT Authentication
    JWT_PRIVATE_KEY_PATH: str = Field(default="/app/secrets/jwt_private.pem")
    JWT_PUBLIC_KEY_PATH: str = Field(default="/app/secrets/jwt_public.pem")
    JWT_ALGORITHM: str = Field(default="RS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)
    JWT_ISSUER: str = Field(default="educational-backend")
    JWT_AUDIENCE: str = Field(default="educational-frontend")
    
    # Security
    SECRET_KEY: str = Field(default="change-me-in-production")
    BCRYPT_ROUNDS: int = Field(default=12)
    
    # CORS
    CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:8080", "http://localhost:3000", "http://127.0.0.1:8080"]
    )
    
    # Observability
    OTEL_SERVICE_NAME: str = Field(default="educational-backend")
    OTEL_EXPORTER_OTLP_ENDPOINT: str = Field(default="http://localhost:4317")
    PROMETHEUS_METRICS_PORT: int = Field(default=9090)
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FORMAT: str = Field(default="json")  # json or console
    
    # Paths
    BASE_DIR: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent.parent)
    
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()