import psycopg2
import os
from dotenv import load_dotenv

# Sets up the connection to the database


def get_connection():

    load_dotenv()
    try:
        conn = psycopg2.connect(database=os.getenv("POSTGRES_DB"),
                                user=os.getenv("POSTGRES_USER"),
                                host=os.getenv("POSTGRES_HOST", "localhost"),
                                password=os.getenv("POSTGRES_PASSWORD"),
                                port=os.getenv("POSTGRES_PORT", 5432))
        return conn
    
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        raise psycopg2.DatabaseError
