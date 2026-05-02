from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:admin@localhost:5432/ecommerce"
    SECRET_KEY: str = "supersecret"
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()