from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    JWT_ACCESS_SECRET_KEY: str = os.getenv("JWT_ACCESS_SECRET_KEY")
    JWT_REFRESH_SECRET_KEY: str = os.getenv("JWT_REFRESH_SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    SENTRY_SDK: str = os.getenv("SENTRY_SDK")
