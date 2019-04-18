from libs import advert


def test_parse_commonfields_list():
    input_ = 'tea,who, you, yeah,bunny'
    expected_ = ['tea', 'who', 'you', 'yeah', 'bunny']
    assert advert._parse_commonfields_list(input_) == expected_
