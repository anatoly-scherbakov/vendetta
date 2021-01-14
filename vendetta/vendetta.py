import csv
from functools import lru_cache
from typing import Callable, Dict, TextIO

from faker import Faker

from vendetta.models import Config, Row, ResponsibleFake, NaiveFake

faker = Faker()


def cached_faker(fake: Callable[[], str]) -> Callable[[str], str]:
    return lru_cache()(lambda _: fake())


class Vendetta:
    """Vendetta context and processor."""

    config: Config
    fakes: Dict[str, ResponsibleFake]

    def __init__(self, config: Config) -> None:
        """Create a new Vendetta."""
        self.config = config

        faker_config = self.config.faker
        self.faker = Faker(locale=faker_config.locale)

        self.fakes = {}

    def construct_fake(self, name: str) -> ResponsibleFake:
        """Construct fake function by given fake name."""
        fake: NaiveFake = getattr(self.faker, name)
        return lru_cache(maxsize=None)(lambda _: fake())

    def get_fake_by_name(self, name: str) -> ResponsibleFake:
        """Retrieve or construct fake."""
        fake = self.fakes.get(name)
        if fake is None:
            fake = self.construct_fake(name)
            self.fakes[name] = fake

        return fake

    def anonymize_file(self, input_file: TextIO, output_file: TextIO) -> None:
        """Anonymize individual file-like object."""
        reader = csv.DictReader(input_file)
        columns = reader.fieldnames

        writer = csv.DictWriter(output_file, fieldnames=columns)
        writer.writeheader()

        fake_per_column = {
            column_name: self.get_fake_by_name(fake_name)
            for column_name, fake_name in self.config.columns
            if column_name in set(columns)
        }

        for row in reader:
            for column_name, fake in fake_per_column.items():
                row[column_name] = fake(row[column_name])

            writer.writerow(row)
