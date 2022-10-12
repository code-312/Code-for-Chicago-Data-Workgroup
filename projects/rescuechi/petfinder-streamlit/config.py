import os
from dotenv import load_dotenv

load_dotenv()

SHOW_QUERIES = os.getenv('PETFINDER_STREAMLIT_SHOW_QUERIES')
CHART_TYPE = os.getenv('PETFINDER_STREAMLIT_CHART_TYPE')
HEROKU_URL = os.getenv('HEROKU_POSTGRESQL_AMBER_URL')
