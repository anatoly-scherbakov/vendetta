import csv
from typing import TextIO, List

from vendetta.models import Row


def parse_csv(input_data: TextIO) -> List[Row]:
    """Parse text CSV data for test purposes."""
    return list(csv.DictReader(input_data))
