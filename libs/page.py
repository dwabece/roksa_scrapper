"""
Logic responsible for fetching ad data from website
"""
import re

import requests
from bs4 import BeautifulSoup

from logmodule import get_logger

LOGGER = get_logger(__name__)


def _get_advert_url(rox_id):
    return f'https://www.roksa.pl/en/advertisements/show/{rox_id}'


def _is_response_really_200(www_body):
    """
    Sometimes server responds with HTTP 200 and '404'-alike content
    so we need to doublecheck that.
    """
    probe_phrase = 'Such an ad does not exist or was disabled.'
    return probe_phrase not in www_body


def _execute_rox_request(advert_url):
    """
    Executes parametrized request to portal
    """
    headers_payload = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'roksapl=ipr25mvvvto0fk2og33cfbn4g5',
        'Host': 'www.roksa.pl',
        'Referer': 'https://www.roksa.pl/',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36',
    }
    request_params = {'headers': headers_payload, 'timeout': 1.5}
    return requests.get(advert_url, **request_params)


def get_rox_page(url):
    """
    Fetching rox page by its url.
    """
    response = _execute_rox_request(url)
    response.raise_for_status()

    page_body = response.content.decode('utf-8')

    return response.status_code, page_body


def get_advert_page(rid):
    """
    Fetching advert page from portal.
    Verifying if response was really 200 or it was just empty page
    with no data returning http 200 status.
    """
    advert_url = _get_advert_url(rid)
    _, page_body = get_rox_page(advert_url)

    if not _is_response_really_200(page_body):
        raise requests.exceptions.HTTPError(f'ad {rid} disabled or deleted')

    return page_body


def get_sresults_page(page_num=None):
    """
    Fetching search results page by its number
    """
    base_url = 'https://www.roksa.pl/pl/szukaj/?anons_type=0&cenaod=1'
    if page_num:
        base_url += f'&pageNr={page_num}'

    _, page_body = get_rox_page(base_url)
    return page_body


def get_sresults_pages_info(page_body):
    """
    Get pagination info (next page and last page number)
    from passed search results page
    """
    soup = BeautifulSoup(page_body, 'html.parser')
    pagination_container = soup.find_all('div', class_='stronnicowanie')

    if not pagination_container:
        raise Exception('no pagination found!')

    pagination_str = pagination_container[0].text
    pages = re.findall(r'\d+', pagination_str)

    pages = [int(p) for p in pages]
    pages[0] += 1

    return pages
