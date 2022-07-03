from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_USERNAME : str
    DATABASE_PASSWORD : str
    DATABASE_NAME : str
    DATABASE_HOSTNAME : str
    DATABASE_PORT : str
    ALGORITHM : str
    SECRET_KEY : str
    ACCESS_TOKEN_EXPIRY_TIME : int

    class Config:
        env_file = ".env"

settings = Settings()