from pydantic import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    geo_user: str
    backend_host: str
    redis_host: str
    app_base_url: str
    pem_file: str
    key_file: str
 
    class Config:
        env_file = ".env"


settings = Settings()
