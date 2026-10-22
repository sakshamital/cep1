"""Configuration classes for DocumentReady."""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
os.makedirs(INSTANCE_DIR, exist_ok=True)


def get_database_uri() -> str:
    """Resolve and normalize database URI, using psycopg2 driver explicitly.

    Render provides postgres:// URLs. SQLAlchemy 2.0+ defaults to psycopg (v3)
    for bare postgresql:// URLs. We pin to psycopg2 since psycopg2-binary is installed.
    """
    uri = os.environ.get("DATABASE_URL")
    if uri:
        if uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql+psycopg2://", 1)
        elif uri.startswith("postgresql://"):
            uri = uri.replace("postgresql://", "postgresql+psycopg2://", 1)
        return uri
    return f"sqlite:///{os.path.join(INSTANCE_DIR, 'documentready.db')}"


class Config:
    """Base configuration."""
    SECRET_KEY: str = os.environ.get("SECRET_KEY") or "dev-key-please-change-in-production"
    JSON_SORT_KEYS: bool = False
    MAX_CONTENT_LENGTH: int = 16 * 1024  # 16 KB for standard JSON API endpoints

    # Database
    SQLALCHEMY_DATABASE_URI: str = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    # Security & Sessions
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = "Lax"
    SESSION_COOKIE_SECURE: bool = os.environ.get("SESSION_COOKIE_SECURE", "False").lower() in ("true", "1")

    # Source Monitoring
    MONITOR_USER_AGENT: str = "DocumentReady-GovMonitor/1.0 (+https://documentready.gov.in/bot)"
    MONITOR_REQUEST_TIMEOUT: int = int(os.environ.get("MONITOR_REQUEST_TIMEOUT", "15"))
    MONITOR_MAX_RETRIES: int = 3
    MONITOR_RATE_LIMIT_DELAY: float = 1.0  # seconds between requests to same domain
    DOWNLOAD_MAX_PDF_BYTES: int = 15 * 1024 * 1024  # 15 MB limit
    DOWNLOAD_DIR: str = os.path.join(INSTANCE_DIR, "downloads")

    # AI / LLM Integration (Optional)
    AI_PROVIDER: str = os.environ.get("AI_PROVIDER", "none")  # none, gemini, openai
    GEMINI_API_KEY: str = os.environ.get("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")

    # Notifications
    SMTP_HOST: str = os.environ.get("SMTP_HOST", "")
    SMTP_PORT: int = int(os.environ.get("SMTP_PORT", "587"))
    SMTP_USER: str = os.environ.get("SMTP_USER", "")
    SMTP_PASSWORD: str = os.environ.get("SMTP_PASSWORD", "")
    NOTIFICATION_FROM_EMAIL: str = os.environ.get("NOTIFICATION_FROM_EMAIL", "notifications@documentready.org")


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG: bool = True


class TestingConfig(Config):
    """Testing configuration."""
    TESTING: bool = True
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG: bool = False
    SESSION_COOKIE_SECURE: bool = True


config_map = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
