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
from validators.url import url
from requests import RequestException
from . import url_check
from . import db_connector
import psycopg2
import os


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
get_connect = psycopg2.connect(DATABASE_URL)


@app.get('/')
def get_start():
    return render_template(
        'index.html',
        messages=get_flashed_messages(with_categories=True),
        url='',
    )


@app.post('/urls')
def add_url():
    adress_dict = request.form.to_dict()
    adress = adress_dict.get('url')
    if not url(adress):
        flash('Некорректный URL', 'danger')
        return render_template(
            'index.html',
            url=adress,
            messages=get_flashed_messages(with_categories=True),
        ), 422
    normalize_url = url_check.get_normalize_url(adress)
    id = db_connector.get_url_id(normalize_url, get_connect)
    if id:
        flash('Страница уже существует', 'secondary')
        return redirect(url_for('show_url', id=id[0],))
    id = db_connector.add_url_data(normalize_url, get_connect)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_url', id=id[0],))


@app.route('/urls/<int:id>')
def show_url(id):
    url = db_connector.get_url_data(id, get_connect)
    check = db_connector.get_check_data(id, get_connect)
    return render_template(
        'url.html',
        messages=get_flashed_messages(with_categories=True),
        url=url,
        checks=check,
    )


@app.get('/urls')
def show_urls():
    checks = db_connector.get_all_urls_data(get_connect)
    return render_template(
        'urls.html',
        checks=checks,
    )


@app.post('/urls/<int:id>/checks')
def get_check(id):
    url_name = db_connector.get_url_data(id, get_connect)['name']
    try:
        url_data = url_check.get_url_check(url_name)
        db_connector.add_check_data(id, url_data, get_connect)
        flash('Страница успешно проверена', 'success')
        return redirect(url_for('show_url', id=id,))
    except RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('show_url', id=id,))
