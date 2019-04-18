"""
Helper functions used by unit tests
"""

import os
from unittest import mock


def mock_response(status=200, content='lorem ipsum hey!', raise_for_status=None):
    """
    Returns mocked `requests.get` response.
    """
    response_mock = mock.Mock()

    response_mock.raise_for_status = mock.Mock()
    if raise_for_status:
        response_mock.raise_for_status.side_effect = raise_for_status
    response_mock.status_code = status
    response_mock.content = bytes(content, 'utf-8')
    return response_mock


def _make_response(http_code, html_file):
    basepath = os.path.dirname(__file__)
    template_file = os.path.join(basepath, 'assets', html_file)

    with open(template_file, 'r') as fobj:
        return http_code, fobj.read()


def response_fake_200():
    """
    Returns `libs.pages.get_rox_page` compatible response,
    containing HTTP response code and html body

    That response if false positive. There are some situations
    when roksa will return HTTP 200 but there will be no ad.
    """
    return _make_response(200, '404.html')


def response_200_tags():
    """
    Returns `libs.pages.get_rox_page` compatible response,
    containing HTTP response code and html body

    Page body contains tags block which contains services
    that worker is providing.
    """
    return _make_response(200, '200_with_tags.html')


def response_search_results():
    """
    Returns search results page.

    Current page is 3, last page num is 218
    """
    return _make_response(200, 'search_results.html')
