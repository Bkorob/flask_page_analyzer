from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests


def get_normalize_url(url):
    prev_adress = urlparse(url)
    return f'{prev_adress.scheme}://{prev_adress.netloc}'


def get_url_check(url):
    response = requests.get(url)
    response.raise_for_status()
    result_dict = get_parse_response(response)
    result_dict['status_code'] = response.status_code
    return result_dict


def get_parse_response(response):
    result = {}
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title')
    result['title'] = title.get_text() if title else ''
    h1 = soup.find('h1')
    result['h1'] = h1.get_text() if h1 else ''
    description = soup.find('meta', {'name': 'description'})
    result['description'] = description['content'] if description else ''
    return result
