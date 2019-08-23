import pytest
from unittest import mock, TestCase
from libs import advert


class TestAdvert(TestCase):

    @pytest.mark.usefixtures('fix_200_w_attrs')
    @mock.patch('requests.get', return_value='fix_200_w_attrs')
    def test_1(self, huj):
        print(huj)