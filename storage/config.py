import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = os.getenv('DATABASE_URI')
DATABASE_URI_TEST = os.getenv('DATABASE_URI_TEST')
SECRET_KEY = os.getenv('SECRET_KEY')