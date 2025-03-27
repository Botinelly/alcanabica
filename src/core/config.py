import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "alcanabica")
