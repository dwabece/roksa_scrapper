import pytest
import requests
from libs import page
from unittest import mock
from tests import helpers


def test_get_advert_page_url():
    expected_url = 'https://www.roksa.pl/en/advertisements/show/1312'
    assert page._get_advert_url(1312) == expected_url


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


@mock.patch('requests.get')
def test_get_rox_page(mock_get):
    resp = helpers.mock_response(content='hey ho!')
    mock_get.return_value = resp

    resp_code, page_body = page.get_rox_page(1337)

    assert resp_code == 200
    assert page_body == 'hey ho!'


@mock.patch('requests.get')
def test_get_rox_page_404(mock_get):
    resp = helpers.mock_response(
        status=404,
        raise_for_status=requests.exceptions.HTTPError('bang')
    )
    mock_get.return_value = resp

    with pytest.raises(requests.exceptions.HTTPError):
        page.get_rox_page(1337)


@mock.patch('libs.page.get_rox_page')
def test_advert_page_200(resp_mock):
    resp_mock.return_value = [200, 'hello!']
    code, page_body = page.get_advert_page(1337)

    assert code == 200
    assert page_body == 'hello!'


@mock.patch('libs.page.get_rox_page')
def test_advert_page_fake_200(resp_mock):
    resp_mock.return_value = helpers.response_fake_200()

    with pytest.raises(requests.exceptions.HTTPError):
        page.get_advert_page(1337)


def test_get_search_results_last_page():
    _, page_body = helpers.response_search_results()

    current_page, max_pages = page.get_sresults_pages_info(page_body)
    assert current_page == 3
    assert max_pages == 218
