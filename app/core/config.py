import os
from dotenv import load_dotenv
from pydantic import BaseSettings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
load_dotenv(os.path.join(BASE_DIR, '.env'))


class Settings(BaseSettings):
    PROJECT_NAME = os.getenv('PROJECT_NAME', 'FASTAPI BASE')
    SECRET_KEY = os.getenv('SECRET_KEY', '')
    API_PREFIX = ''
    BACKEND_CORS_ORIGINS = ['*']
    DATABASE_URL = os.getenv('SQL_DATABASE_URL', '')
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # Token expired after 7 days
    SECURITY_ALGORITHM = 'HS256'
    LOGGING_CONFIG_FILE = os.path.join(BASE_DIR, 'logging.ini')
    BACKEND_HOST = os.getenv('BACKEND_HOST', 'http://localhost:8000')
    # ADMIN DEFAULT INFO
    DEFAULT_ADMIN_EMAIL = os.getenv('DEFAULT_ADMIN_EMAIL')
    DEFAULT_ADMIN_PASSWORD = os.getenv('DEFAULT_ADMIN_PASSWORD')
    DEFAULT_ADMIN_FULL_NAME = os.getenv('DEFAULT_ADMIN_FULL_NAME')
    DEFAULT_ADMIN_PHONE = os.getenv('DEFAULT_ADMIN_PHONE')
    OTP_EXPIRES_IN = os.getenv('OTP_EXPIRES_IN', 60 * 5)

    class Config:
        env_file = ".env"


settings = Settings()
