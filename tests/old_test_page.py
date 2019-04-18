from unittest import mock
from libs import page
from tests import helpers
import pytest
import requests

mocked_requests_get = {}


def test_get_page_url():
    expected = 'https://www.roksa.pl/en/advertisements/show/123'
    assert page._get_advert_url(123) == expected


def test_is_response_really_200():
    _, html_body = helpers.response_fake_200()
    assert page._is_response_really_200(html_body) == False


@mock.patch('requests.get')
def test_execute_rox_request(request_get):
    url = page._get_advert_url(1337)
    page._execute_rox_request(url)

    expected_request_params = {
        'headers': {'Referer': 'https://www.roksa.pl/'},
        'timeout': 1.5,
    }
    expected_url = 'https://www.roksa.pl/en/advertisements/show/1337'

    request_get.assert_called_with(expected_url, **expected_request_params)


@mock.patch('libs.page.get_rox_page', helpers.response_200_tags(True))
def test_get_advert_page_ok():
    exp_code, exp_body = helpers.response_200_tags()
    code, res = page.get_advert_page(200)

    assert code == exp_code
    assert res == exp_body


@mock.patch('libs.page.get_rox_page', helpers.response_404(True))
def test_get_advert_page_not_found():
    exp_code, exp_body = helpers.response_404()
    with pytest.raises(requests.exceptions.HTTPError):
        page.get_advert_page(404)


@mock.patch('libs.page.get_rox_page', helpers.response_fake_200(True))
def test_get_advert_page_fake_200():
    with pytest.raises(requests.exceptions.HTTPError):
        helpers.response_fake_200()


def test_search_results_page():
    response_page_body = page.get_sresults_page(1985)
