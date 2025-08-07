import os

from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_USER = os.getenv("REDIS_USER")
REDIS_PWD = os.getenv("REDIS_PWD")

OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")