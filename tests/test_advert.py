import pytest
from libs import advert


advert_200_desc = (
    'Witam serdecznie oraz zapraszam do siebie gentlemanów niezależnie od '
    'wieku. Każdego mężczyznę traktuje indywidualnie, z należytym szacunkiem. '
    'Czy zawsze marzyłeś o pięknej kobiecie która jest podziwiana i pożądana, '
    'ale nie wiedziałeś gdzie ją znaleźć? W takim razie już znalazłeś - '
    'jestem zmysłową kobietą, która chętnie dotrzyma Tobie towarzystwa, jak '
    'również przeżyjesz ze mną namiętną przygodę. Oferuję czułość i '
    'namiętność na każdej naszej randce, bez pośpiechu, zadbam o Ciebie. '
    'Przekonasz się jakie cudowne chwile spędzimy razem. Będziesz delektował '
    'się każdą chwilą spędzoną w moim towarzystwie.... Propozycję moją '
    'kieruję do kulturalnych Panów, szukających relaksu i przyjemnego '
    'oderwania od rzeczywistości. Panów, którzy pragną przeżyć chwile '
    'zapomnienia w ramionach zmysłowej kochanki, nieszczędzącej uśmiechów, '
    'pocałunków i wielu innych przyjemności, jakich kobieta i mężczyzna mogą '
    'doświadczyć. Moje ogłoszenie jest w 100 procentach prywatne na spotkaniu '
    'jesteśmy sami, a zdjęcia przedstawiają moją osobę . Telefony odbieram '
    'osobiście, zatem proszę o wyrozumiałość, jeśli w podanym czasie nie '
    'możesz się ze mną połączyć Zapraszam Maja'
)

advert_200_expected_commonfields = {
    'city': 'łódź',
    'district': 'centrum',
    'out_calls': 'only to hotels',
    'age': '42',
    'weight': '55',
    'height': '168',
    'breast': '3',
    'languages': [],
    'price_hour': '130',
    'price_quarter': '80',
    'price_half': '100',
    'price_night': '1200',
    'phone_number': '511626694'
}

advert_200_expected_services = [
    'wielokrotność', 'francuski bez zabezpieczenia',
    'masaż relaksacyjny', '69', 'pieszczoty', 'pocałunki',
    'miłość hiszpańska', 'wspólna masturbacja', 'fetysz stóp',
    'analny w stronę partnera (dopłata)', 'finał do buzi (dopłata)',
    'finał na ciałko', 'towarzystwo', 'gfe', 'footjob', 'dowolność pozycji',
    'sexy bielizna', 'szpilki', 'pończoszki', 'higiena', 'prywatnie',
    'dyskretnie', 'pissing (dopłata)', 'delikatny rimming (dopłata)',
    'zabawa z wibratorem (dopłata)', 'crossdressing(dopłata)',
]


def _make_advert_200_fields():
    fields = {}
    fields.update(advert_200_expected_commonfields)
    ad = {
        'rid': '439861',
        'name': 'Czarna Perła',
        'services': advert_200_expected_services,
        'description': advert_200_desc
    }
    fields.update(ad)

    return fields


@pytest.mark.usefixtures('fix_200_w_attrs_soup')
def test_get_ad_basic_fields(fix_200_w_attrs_soup):
    """
    Test that covers fetching `easy to get` fields, that
    requires' not much of processing, just simple BS query

    """
    ad_id = advert._get_ad_id(fix_200_w_attrs_soup)
    assert '439861' == ad_id

    ad_name = advert._get_ad_name(fix_200_w_attrs_soup)
    assert 'Czarna Perła' == ad_name

    ad_desc = advert._get_ad_description(fix_200_w_attrs_soup)
    assert advert_200_desc == ad_desc


@pytest.mark.usefixtures('fix_200_w_attrs_soup')
def test_get_services(fix_200_w_attrs_soup):
    assert advert_200_expected_services == advert._get_services(fix_200_w_attrs_soup)


@pytest.mark.usefixtures('fix_200_w_attrs_soup')
def test_attrs_commonfields(fix_200_w_attrs_soup):
    assert advert_200_expected_commonfields == advert._get_commonfields(fix_200_w_attrs_soup)


@pytest.mark.usefixtures('fix_200_w_attrs')
def test_get_ad(fix_200_w_attrs):
    ad_fields = _make_advert_200_fields()

    assert ad_fields == advert._parse_ad(fix_200_w_attrs)
