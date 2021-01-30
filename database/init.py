"""Script creating database schema"""
import os

from dotenv import load_dotenv
import psycopg2

load_dotenv()

host = os.getenv("host")
database = os.getenv("database")
user = os.getenv("user")
port = os.getenv("port")
password = os.getenv("password")

conn = psycopg2.connect(
    host=host, database=database, user=user, port=port, password=password
)
cur = conn.cursor()

cur.execute(
    "\
    CREATE TABLE history \
    (id serial PRIMARY KEY, features text,\
    prediction text, date date);"
)

conn.commit()