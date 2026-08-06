import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(database=os.getenv("POSTGRES_DB"),
                        user=os.getenv("POSTGRES_USER"),
                        host=os.getenv("POSTGRES_HOST", "localhost"),
                        password=os.getenv("POSTGRES_PASSWORD"),
                        port=os.getenv("POSTGRES_PORT", 5432))
