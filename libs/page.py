"""
Logic responsible for fetching ad data from website
"""

import requests
from logmodule import get_logger

logger = get_logger(__name__)


def _get_advert_url(rox_id):
    return f'https://www.roksa.pl/en/advertisements/show/{rox_id}'


def _is_response_really_200(www_body):
    """
    Sometimes server responds with HTTP 200 and '404'-alike content
    so we need to doublecheck that.
    """
    probe_phrase = 'Such an ad does not exist or was disabled.'
    return True if probe_phrase not in www_body else False


def _execute_rox_request(rid):
    """
    Executes parametrized request to portal
    """
    advert_url = _get_advert_url(rid)

    headers_payload = {
        'Referer': 'https://www.roksa.pl/',
    }
    request_params = {
        'headers': headers_payload,
        'timeout': 0.5,
    }
    return requests.get(advert_url, **request_params)


def call_rox_advert(rid):
    """
    Fetching advert page from portal.
    Verifying if response was really 200 or it was just empty page
    with no data returning http 200 status.
    """
    response = _execute_rox_request(rid)
    response.raise_for_status()

    http_response_code = response.status_code
    page_body = response.content.decode('utf-8')

    if not _is_response_really_200(page_body):
        raise requests.exceptions.HTTPError(f'ad {rid} disabled or deleted')

    return http_response_code, page_body
