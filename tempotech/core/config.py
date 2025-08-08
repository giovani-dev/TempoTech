import os

from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_USER = os.getenv("REDIS_USER")
REDIS_PWD = os.getenv("REDIS_PWD")

OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")

DB_ENGINE = os.getenv("DB_ENGINE")

DB_USER = os.getenv("DB_USER")
DB_PWD = os.getenv("DB_PWD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
