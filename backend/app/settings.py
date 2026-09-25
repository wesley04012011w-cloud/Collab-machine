from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Collab Machine"
    app_env: str = "development"
    app_url: str = "http://localhost:8000"
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "http://localhost:8000/api/v1/auth/google/callback"
    colab_api_enabled: bool = False
    ollama_base_url: str = "http://127.0.0.1:11434"
    session_secret: str = "change-me"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
