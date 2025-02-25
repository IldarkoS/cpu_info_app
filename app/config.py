from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST :str
    DB_PORT :int
    DB_NAME :str
    DB_USER :str
    DB_PASS :str

    class Config:
        env_file = ".env"


settings = Settings()

settings.__dict__['DATABASE_URL'] = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"