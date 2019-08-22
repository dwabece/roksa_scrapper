from unittest import mock, TestCase
import pytest
import requests
from libs import page


class PageTest(TestCase):
    @staticmethod
    def _mock_response(
            status=200,
            content="CONTENT",
            json_data=None,
            headers={},
            raise_for_status=None):
        resp = mock.Mock()
        resp.raise_for_status = mock.Mock()
        if raise_for_status:
            resp.raise_for_status.side_effect = raise_for_status
        resp.status_code = status
        resp.content = content
        resp.headers = headers
        if json_data:
            resp.json = mock.Mock(
                return_value=json_data
            )
        return resp

    @mock.patch('requests.get')
    def test_execute_rox_request(self, request_get):
        url = page._get_advert_url(1337)
        page._execute_rox_request(url)

        expected_request_params = {
            'headers': {'Referer': 'https://www.roksa.pl/'},
            'timeout': 1.5,
        }
        expected_url = 'https://www.roksa.pl/en/advertisements/show/1337'

        assert expected_url == url

        request_get.assert_called_with(expected_url, **expected_request_params)

    @mock.patch('libs.page.requests.get')
    def test_get_page_200(self, requests_get):
        requests_get.return_value = PageTest._mock_response(content=b'hey!')
        status_code, body = page.get_rox_page('http://url.tld/ad/numb3r')

        assert (200, 'hey!') == (status_code, body)

    @mock.patch('libs.page.requests.get')
    def test_get_advert_page_fake200(self, requests_get):
        requests_get.return_value = PageTest._mock_response(
            content=b'Such an ad does not exist or was disabled.'
        )

        with pytest.raises(requests.exceptions.HTTPError):
            page.get_advert_page(1337)

    # @mock.patch('libs.page.requests.get')
    # def test_get_rox_page_404(mock_get, requests_get):
    #     requests_get.return_value = PageTest._mock_response(
    #         status=404,
    #         content=b'asd',
    #         raise_for_status=requests.exceptions.HTTPError()
    #     )

    #     with pytest.raises(requests.exceptions.HTTPError):
    #         page.get_rox_page('http://that-will-give-404')
