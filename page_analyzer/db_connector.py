from dotenv import load_dotenv
from datetime import datetime
from psycopg2.extras import RealDictCursor
import psycopg2
import os


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
CONN = psycopg2.connect(DATABASE_URL)


def add_url_data(url, conn=CONN):
    with conn.cursor() as cur:
        cur.execute(
            '''INSERT INTO urls (name, created_at)
            VALUES (%s, %s) RETURNING id''',
            (url, datetime.now(),),
        )
        id = cur.fetchone()
        conn.commit()
    conn.close()    
    return id


def get_url_id(url, conn=CONN):
    with conn.cursor() as cur:
        cur.execute(
            '''SELECT id FROM urls
            WHERE name = %s''',
            (url,))
        result = cur.fetchone()
    conn.close()
    return result


def get_url_data(id, conn=CONN):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            '''SELECT * FROM urls WHERE id = %s''',
            (id,),
        )
        url_data = cur.fetchone()
        conn.commit()
    conn.close()    
    return url_data


def get_check_data(id, conn=CONN):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            '''SELECT * FROM url_checks WHERE url_id = %s''',
            (id,),
        )
        check_data = cur.fetchall()
        conn.commit()
    conn.close()
    return check_data


def add_check_data(id, url_data, conn=CONN):
    url_data['id'] = id
    url_data['created_at'] = datetime.now()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            '''INSERT INTO url_checks (
                url_id,
                status_code,
                h1,
                title,
                description,
                created_at)
                VALUES (
                    %(id)s,
                    %(status_code)s,
                    %(h1)s,
                    %(title)s,
                    %(description)s,
                    %(created_at)s)''',
            (url_data),)
        conn.commit()
        cur.close()
    return


def get_all_urls_data(conn=CONN):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute('''
                    SELECT distinct on (urls.id)
                    urls.id,
                    urls.name,
                    url_checks.created_at,
                    url_checks.status_code
                    FROM urls LEFT JOIN url_checks
                    ON urls.id=url_checks.url_id
                    ''')
        result_dict = cur.fetchall()
        conn.commit()
    conn.close()
    return result_dict
