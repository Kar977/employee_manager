from pydantic_settings import BaseSettings

from pydantic import Field

class Settings(BaseSettings):
    postgres_user: str = Field(default="postgres")
    postgres_password: str = Field(default="password")
    postgres_host: str = Field(default="employee-db")
    postgres_port: str = Field(default="5432")
    postgres_name: str = Field(default="postgres_employee")


settings = Settings()