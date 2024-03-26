from dotenv import load_dotenv
from datetime import datetime
from psycopg2.extras import RealDictCursor
import psycopg2
import os


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
CONN = psycopg2.connect(DATABASE_URL)


def add_url_data(url, conn=CONN):
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                '''INSERT INTO urls (name, created_at)
                VALUES (%s, %s)''',
                (url, datetime.now(),),
            )
        conn.commit()
        result = get_url_id(url)
        return result  
    except psycopg2.errors.UniqueViolation:
        result = get_url_id(url)
        result['id'] = cur.fetchone()['id']
        result['flash'] = ['Страница уже существует', 'secondary']
        return result
        
print(add_url_data('https://jsiqoo.com'))

def get_url_id(url, conn=CONN):
    result = {}
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            '''SELECT id FROM urls
            WHERE name = %s''',
            (url,))
        id = cur.fetchone()['id']
        result['flash'] = ['Страница успешно добавлена', 'success']
        result['id'] = cur.fetchone()['id']
        conn.commit()
        return result


def get_url_data(id, conn=CONN):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            '''SELECT * FROM urls WHERE id = %s''',
            (id,),
        )
        url_data = cur.fetchone()
        conn.commit()
        return url_data


def get_check_data(id, conn=CONN):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            '''SELECT * FROM url_checks WHERE url_id = %s''',
            (id,),
        )
        check_data = cur.fetchall()
        conn.commit()
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
        return result_dict
            