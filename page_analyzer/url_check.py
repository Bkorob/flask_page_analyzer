import requests
from requests import RequestException


def get_url_check(url):
    result = {}
    try:
        response = requests.get(url)
        result['status_code'] = response.status_code
        return result
    except RequestException as re:
        raise SystemExit(re)
