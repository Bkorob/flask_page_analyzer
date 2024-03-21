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
import os
import psycopg2
from datetime import datetime


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
        messages=get_flashed_messages(),
        url={},
    )


@app.post('/urls')
def add_url():
    adress_dict = request.form.to_dict()
    adress = adress_dict.get('url')
    if not url_check(adress):
        flash(' Hеверный формат URL')
        return render_template(
            'index.html',
            url=adress_dict,
            messages=get_flashed_messages(),
        )
    prev_adress = urlparse(adress)
    normalize_url = prev_adress.netloc
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    '''INSERT INTO urls (name, created_at)
                    VALUES (%s, %s) RETURNING id;''',
                    (normalize_url, datetime.now()),
                )
                flash('URL успешно добавлен')
                id = cur.fetchone()[0]
                return redirect(url_for('show_url', id=id))
    except psycopg2.errors.UniqueViolation:
        with get_conn() as conn:
            with conn.cursor() as curs:
                curs.execute(
                    '''SELECT id FROM urls 
                    WHERE name=(%s);''', 
                    (normalize_url,))
                flash('такой URL уже существует')
                id = curs.fetchone()[0]
                return redirect(url_for('show_url', id=id))



@app.route('/urls/<id>')
def show_url(id):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                '''SELECT * FROM urls WHERE id = (%s);''',
                (id,),
            )
            url = cur.fetchall()
            return render_template(
                'url.html',
                messages=get_flashed_messages(),
                url=url,
            )


@app.get('/urls')
def show_urls():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                '''
                SELECT * FROM urls 
                ORDER BY created_at DESC;
                '''
            )
            urls = cur.fetchall()
            return render_template(
                'urls.html',
                urls = urls,
            )