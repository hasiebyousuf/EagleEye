from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Looks for .env in current dir (Docker) or parent dir (local dev from backend/)
    model_config = SettingsConfigDict(env_file=(".env", "../.env"), extra="ignore")

    supabase_url: str
    supabase_service_key: str
    supabase_anon_key: str
    kimi_api_key: str
    google_trends_api_key: str
    serpapi_key: str


settings = Settings()
