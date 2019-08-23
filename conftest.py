import os
import pytest


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
