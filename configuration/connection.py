from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class POSTGRESDB(BaseSettings):
    USERNAME1:  str = os.environ["POSTGRES_USERNAME"]
    PASSWORD: str = os.environ["POSTGRES_PASSWORD"]
    HOST:  str = os.environ["POSTGRES_HOST"]
    PORT:  str = os.environ["POSTGRES_PORT"]
    SCHEMA: str = os.environ["POSTGRES_SCHEMA"]