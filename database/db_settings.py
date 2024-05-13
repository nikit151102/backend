from dotenv import load_dotenv
import os

class Settings:
    app_name: str = "New API"
    admin_email: str = "nikit5090@gmail.com"
    DATABASE_URL: str
    POSTGRES_DATABASE_URLS: str
    POSTGRES_DATABASE_URLA: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

# settings = Settings()
# settings.POSTGRES_HOST = 'db'  
# settings.POSTGRES_PORT = 5432
# settings.POSTGRES_PASSWORD = 'root'
# settings.POSTGRES_USER = 'root' 
# settings.POSTGRES_DB = 'vitkon'
    
settings = Settings()
settings.POSTGRES_HOST = 'localhost' 
settings.POSTGRES_PORT = 5432
settings.POSTGRES_PASSWORD = 'nikit5090'
settings.POSTGRES_USER = 'postgres' 
settings.POSTGRES_DB = 'vitkon'


settings.POSTGRES_DATABASE_URLA = f"postgresql+asyncpg://" \
                                f"{settings.POSTGRES_USER}:" \
                                f"{settings.POSTGRES_PASSWORD}@" \
                                f"{settings.POSTGRES_HOST}:" \
                                f"{settings.POSTGRES_PORT}/" \
                                f"{settings.POSTGRES_DB}"
settings.POSTGRES_DATABASE_URLS = f"postgresql://" \
                                f"{settings.POSTGRES_USER}:" \
                                f"{settings.POSTGRES_PASSWORD}@" \
                                f"{settings.POSTGRES_HOST}:" \
                                f"{settings.POSTGRES_PORT}/" \
                                f"{settings.POSTGRES_DB}"
