from pydantic import EmailStr, SecretStr, HttpUrl, DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    db_uri: str
    debug: bool
    base_url: HttpUrl
    mail_username: str
    mail_password: SecretStr
    mail_host: str
    mail_port: int
    mail_from: EmailStr
    upload_dir: DirectoryPath

    model_config = SettingsConfigDict(env_file=".env")
