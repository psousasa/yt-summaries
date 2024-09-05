import os
from dotenv import load_dotenv

os.environ["RUN_TIMEZONE_CHECK"] = "0"

from db.handler import init_db

print("Initializing database...")
init_db()
