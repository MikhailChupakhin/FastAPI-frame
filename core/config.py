# C:\Users\user1\PycharmProjects\FastAPi-actual\core\config.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_user: str
    db_pass: str
    db_host: str
    db_port: str
    db_name: str

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings(_env_file=".env")

# from dotenv import load_dotenv
# import os
#
# load_dotenv()
#
# DB_USER = os.getenv("DB_USER")
# DB_PASS = os.getenv("DB_PASS")
# DB_HOST = os.getenv("DB_HOST")
# DB_PORT = os.getenv("DB_PORT")
# DB_NAME = os.getenv("DB_NAME")
