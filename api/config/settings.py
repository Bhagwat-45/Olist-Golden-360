from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    db_user : str = Field(alias="DB_USER")
    db_password : str = Field(alias="DB_PASSWORD")
    db_port : int = Field(alias="DB_PORT",default=5432)
    db_host : str = Field(alias="DB_HOST",default="localhost")
    db_name : str = Field(alias="DB_NAME",default="golden_360")

    @property
    def database_url(self)->str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    model_config = SettingsConfigDict(env_file=".env",extra="ignore")

settings = Settings()