import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(dotenv_path="D:/AI_Coach/backend/app/db/.env")

def get_conn():
    return psycopg2.connect(
        dbname="scan_ocr",
        user="postgres",
        password="tldk2247",
        host="localhost",
        port="5432"
    )
