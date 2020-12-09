from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    APP_NAME: str = "boilerplate-fastapi"
    ENVIRON: str

    # dbs
    BOILERPLATE_DATABASE_URI: str
