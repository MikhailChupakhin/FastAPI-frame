# C:\Users\user1\PycharmProjects\FastAPi-actual\core\config.py
import os
from pydantic import BaseModel
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem/"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem/"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 3


class DBSettings(BaseModel):
    db_user: str
    db_pass: str
    db_host: str
    db_port: str
    db_name: str

    def db_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"


class Settings(BaseModel):
    db_settings: DBSettings = DBSettings(
        db_user=DB_USER,
        db_pass=DB_PASS,
        db_host=DB_HOST,
        db_port=DB_PORT,
        db_name=DB_NAME,
    )
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings(_env_file=".env")
