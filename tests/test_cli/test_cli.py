import subprocess
import tempfile
from pathlib import Path

from tests.parse_csv import parse_csv


def test_cli(test_data: Path):
    """Run the project's CLI and test it."""
    with tempfile.TemporaryDirectory() as temp:
        config = test_data / 'config.yaml'
        source = test_data / 'people.csv'
        destination = Path(temp) / 'output.csv'

        subprocess.call([
            'vendetta',
            str(config),
            str(source),
            str(destination)
        ])

        with destination.open() as test_result:
            test_result_data = parse_csv(test_result)

    first, second = test_result_data
    assert first['lastname'] == second['lastname']
    assert first['city'] == second['city']

    assert first['email'] != second['email']
    assert first['phone'] != second['phone']
    assert first['firstname'] != second['firstname']
