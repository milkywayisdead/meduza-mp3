import requests

MEDUZA_URL = 'https://meduza.io'
MEDUZA_NEWS = f'{MEDUZA_URL}/api/w5/search?chrono=news&page=0&locale=ru'

_DT_FMT = '%H:%M %d-%m-%Y'


def get_news_urls(per_page=10):
    """
    Получение url новостей с главной.
    """

    resp = requests.get(f'{MEDUZA_NEWS}&per_page={per_page}')
    resp = resp.json()

    urls = []
    for n, d in resp['documents'].items():
        try:
            d['title']
        except KeyError:
            continue
        urls.append(d['url'])

    return urls

def get_news(url):
    """
    Получение словарей с инфой по новости.

    url - значение url, полученное get_news_urls.
    """

    resp = requests.get(f'{MEDUZA_URL}/api/w5/{url}')
    resp = resp.json()

    blocks = resp['root']['content']['blocks']
    content = ''
    for block in blocks:
        try:
            data = block['data']
        except KeyError:
            continue
        if type(data) is str:
            content += f'{data}\n'

    return {
        'url': url,
        'title': resp['root']['title'],
        'datetime': resp['root']['datetime'],
        'content': content,
    }

def get_news_mul(urls_list):
    """
    Получение словарей с инфой по нескольким новостям.

    urls_lsit - список url, полученных get_news_urls.
    """

    news = []

    for url in urls_list:
        try:
            news.append(get_news(url))
        except KeyError:
            # добавить обработку текстов из /slides/
            print(url)

    return news