import os
import pytest
from bs4 import BeautifulSoup


def _load_html_fixture(fixname):
    here = os.path.abspath(os.path.dirname(__file__))
    fix_path = os.path.join(here, 'tests', 'assets', fixname)

    with open(fix_path, 'r') as r:
        return r.read()


@pytest.fixture
def fix_200_w_attrs():
    """
    fixture that contains pixtures, description
    and left hand side attributes
    """
    return _load_html_fixture('200_w_desc_attrs.html')


@pytest.fixture
def fix_200_w_attrs_soup():
    return BeautifulSoup(
        _load_html_fixture('200_w_desc_attrs.html'),
        'html.parser'
    )


@pytest.fixture()
def fix_elo():
    return {'elo': 123}
