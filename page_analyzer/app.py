from flask import (
    Flask,
    request,
    render_template,
    flash,
    redirect,
    url_for,
    get_flashed_messages,
)
from dotenv import load_dotenv
from urllib.parse import urlparse
from validators.url import url as url_check
from datetime import datetime
from psycopg2.extras import RealDictCursor
import os
import psycopg2


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


def get_conn():
    return psycopg2.connect(DATABASE_URL)


@app.get('/')
def hello_world():
    return render_template(
        'index.html',
        messages=get_flashed_messages(with_categories=True),
        url='',
    )


# обработка формы создающей новую запись в таблице urls
@app.post('/urls')
def add_url():
    adress_dict = request.form.to_dict()
    adress = adress_dict.get('url')
    if not url_check(adress):
        flash(' Hеверный формат URL', 'danger')
        return render_template(
            'index.html',
            url=adress,
            messages=get_flashed_messages(with_categories=True),
        )
    prev_adress = urlparse(adress)
    normalize_url = f'{prev_adress.scheme}://{prev_adress.netloc}'
    try:
        with get_conn() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    '''INSERT INTO urls (name, created_at)
                    VALUES (%s, %s) RETURNING id''',
                    (normalize_url, datetime.now(),),
                )
                flash(' URL успешно добавлен', 'success')
                id = cur.fetchone()['id']
                return redirect(url_for('show_url', id=id))
    except psycopg2.errors.UniqueViolation:
        with get_conn() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as curs:
                curs.execute(
                    '''SELECT id FROM urls
                    WHERE name = %s''',
                    (normalize_url,))
                flash(' Такой URL уже существует', 'secondary')
                id = curs.fetchone()['id']
                return redirect(url_for('show_url', id=id))


@app.route('/urls/<int:id>')
def show_url(id):
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                '''SELECT * FROM urls WHERE id = %s''',
                (id,),
            )
            url = cur.fetchone()
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                '''SELECT * FROM url_checks WHERE url_id = %s''',
                (id,),
            )
            check = cur.fetchall()
            return render_template(
                'url.html',
                messages=get_flashed_messages(with_categories=True),
                url=url,
                checks=check,
            )


@app.get('/urls')
def show_urls():
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('''
                    SELECT distinct on (urls.id)
                    urls.id,
                    urls.name,
                    url_checks.created_at,
                    url_checks.status_code
                    FROM urls LEFT JOIN url_checks
                    ON urls.id=url_checks.url_id
                    ORDER BY urls.id DESC
                    ''')
            checks = cur.fetchall()
            return render_template(
                'urls.html',
                checks=checks,
            )


@app.post('/urls/<int:id>/checks')
def get_check(id):
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                '''INSERT INTO url_checks (url_id, created_at)
                VALUES (%s, %s)''', (id, datetime.now(),),)
            flash('Страница успешно проверена', 'success')
            return redirect(url_for('show_url', id=id))
