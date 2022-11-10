import os
from dotenv import load_dotenv

load_dotenv()

PETFINDER_KEY = os.getenv('PETFINDER_KEY')
PETFINDER_SECRET = os.getenv('PETFINDER_SECRET')
DATABASE_URL = os.getenv('DATABASE_URL')
HEROKU_URL = os.getenv('HEROKU_POSTGRESQL_AMBER_URL')
