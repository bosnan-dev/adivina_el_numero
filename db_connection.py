import psycopg2 as postgres
import os
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

def db_connection():
     try:
          conn = postgres.connect(
               host=os.getenv("DATABASE_URL"),
               database=os.getenv("PG_DATABASE"),
               user=os.getenv("PG_USER"),
               password=os.getenv("PG_PASSWORD"),
               port=os.getenv("PG_PORT", "5432")
          )
          return conn, conn.cursor()
     except Exception as e:
          raise Exception(f"Error al conectar a la base de datos: {e}")
