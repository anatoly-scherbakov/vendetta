from pathlib import Path

from io import StringIO

from tests.parse_csv import parse_csv
from vendetta import Config, Vendetta


def test_vendetta_single(test_data: Path):
    config = Config(columns={
        'firstname': 'first_name',
        'lastname': 'last_name',
        'birthday': 'date',
        'address': 'street_address',
        'city': 'city',
        'state': 'state',
        'country': 'country',
        'email': 'email',
        'phone': 'phone_number',
    })

    v = Vendetta(config=config)

    output_file = StringIO()
    with (test_data / 'people.csv').open('r') as input_file:
        v(input_file, output_file)

    output_file.seek(0)
    output_data = parse_csv(output_file)

    first, second = output_data
    assert first['lastname'] == second['lastname']
    assert first['city'] == second['city']

    assert first['email'] != second['email']
    assert first['phone'] != second['phone']
    assert first['firstname'] != second['firstname']
