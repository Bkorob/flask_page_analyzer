import requests
from requests import RequestException


def get_url_check(url):
    result = {}
    response = requests.get(url)
    response.raise_for_status()
    result['status_code'] = response.status_code
    return result
