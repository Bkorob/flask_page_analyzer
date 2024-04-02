from datetime import datetime
from psycopg2.extras import RealDictCursor


def add_url_data(url, conn):
    with conn.cursor() as cur:
        cur.execute(
            '''INSERT INTO urls (name, created_at)
            VALUES (%s, %s) RETURNING id''',
            (url, datetime.now(),),
        )
        id = cur.fetchone()
        conn.commit()
        return id


def get_url_id(url, conn):
    with conn.cursor() as cur:
        cur.execute(
            '''SELECT id FROM urls
            WHERE name = %s''',
            (url,))
        result = cur.fetchone()
        return result


def get_url_data(id, conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            '''SELECT * FROM urls WHERE id = %s''',
            (id,),
        )
        url_data = cur.fetchone()
        return url_data


def get_check_data(id, conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            '''SELECT * FROM url_checks WHERE url_id = %s''',
            (id,),
        )
        check_data = cur.fetchall()
        return check_data


def add_check_data(id, url_data, conn):
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
        return


def get_all_urls_data(conn):
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
        return result_dict
