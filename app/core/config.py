from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str ="AURIX"
    admin_email: str = "arjunbhattarai860@gmail.com"
    api_version: str = "v1"
    vehicle_backend: str = "simulation"
    debug: bool = False


    class Config:
        model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
        )


settings = Settings()        