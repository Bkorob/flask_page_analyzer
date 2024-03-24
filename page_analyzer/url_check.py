from bs4 import BeautifulSoup
import requests


def get_url_check(url):
    result = {}
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title')
    result['title'] = title.get_text() if title else ''
    h1 = soup.find('h1')
    result['h1'] = h1.get_text() if h1 else ''
    description = soup.find('meta', {'name': 'description'})
    result['description'] = description['content'] if description else ''
    result['status_code'] = response.status_code
    return result
