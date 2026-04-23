import os
from dotenv import load_dotenv

load_dotenv()

class MoviesDbCreds:
    HOST = os.environ["DB_MOVIES_HOST"]
    PORT = int(os.environ["DB_MOVIES_PORT"])
    DATABASE_NAME = os.environ["DB_MOVIES_NAME"]
    USERNAME = os.environ["DB_MOVIES_USERNAME"]
    PASSWORD = os.environ["DB_MOVIES_PASSWORD"]