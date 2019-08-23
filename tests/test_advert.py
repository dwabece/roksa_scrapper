import pytest
from unittest import mock
from libs import advert


@pytest.mark.usefixtures('fix_200_w_attrs_soup')
def test_get_ad_basic_fields(fix_200_w_attrs_soup):
    """
    Test that covers fetching `easy to get` fields, that
    requires' not much of processing, just simple BS query

    """
    ad_id = advert._get_ad_id(fix_200_w_attrs_soup)
    assert '439861' == ad_id


