from dotenv import load_dotenv
from datetime import datetime
from psycopg2.extras import RealDictCursor
import psycopg2
import os


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
CONN = psycopg2.connect(DATABASE_URL)


def add_url_data(url, conn=CONN):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            '''INSERT INTO urls (name, created_at)
            VALUES (%s, %s)''',
            (url, datetime.now(),),
        )
        conn.commit()


def get_url_id(url, conn=CONN):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            '''SELECT id FROM urls
            WHERE name = %s''',
            (url,))
        id = cur.fetchone()['id']
        conn.commit()
        return id