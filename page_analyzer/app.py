from flask import Flask, request, render_template, flash, redirect
from dotenv import load_dotenv
from psycopg2.extras import NamedTupleCursor
from urllib.parse import urlparse
from validators.url import url
import os
import psycopg2
from datetime import datetime



load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.post('/urls')
def add_urls():
    if url(request.form.get('url')):
        adress = request.form.get('url')
        if urlparse(adress):
            with conn.cursor() as cur:
                cur.execute(
                    '''INSERT INTO urls (name, created_at) 
                    VALUES (%s, %s);''',
                    (adress, datetime.now()),
                  )
                cur.execute(
                     '''SELECT id FROM urls WHERE name = (%s);''',
                     (adress)
                )
                id = cur.fetchall()
                return render_template(
                'urls.html', id = id
            )


# @app.route('/urls/<int:id>')
# def show_urls(id):
    # return 'hello'+ id
#         flash('Невалидный адрес')
#         return redirect('/')