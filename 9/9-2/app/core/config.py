""" DOC """

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """ DOC """

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def async_database_url(self):
        """ DOC """

        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@ \
            {self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        """ DOC """

        env_file = ".env"


settings = Settings()
