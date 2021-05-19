import csv
from functools import lru_cache
from typing import Dict, TextIO

from faker import Faker

from vendetta.models import Config, NaiveFake, ResponsibleFake


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

        if not columns:
            raise ValueError('The source file has no columns.')

        writer = csv.DictWriter(output_file, fieldnames=columns)
        writer.writeheader()

        fake_per_column = {
            column_name: self.get_fake_by_name(fake_name)
            for column_name, fake_name in self.config.columns.items()
            if column_name in set(columns)
        }

        for row in reader:
            for column_name, fake in fake_per_column.items():
                row[column_name] = fake(row[column_name])

            writer.writerow(row)

    def print_untouched(self, input_file: TextIO, output_file: TextIO) -> None:
        """Print the data untouched by the config."""
        reader = csv.DictReader(input_file)
        columns = reader.fieldnames

        touched_columns = set(self.config.columns.keys())
        untouched_columns = [
            column for column in columns
            if column not in touched_columns
        ]

        if not untouched_columns:
            return

        writer = csv.DictWriter(output_file, fieldnames=untouched_columns)
        writer.writeheader()

        untouched_columns_set = set(untouched_columns)
        for row in reader:
            sliced_row = {
                column_name: column_value
                for column_name, column_value
                in row.items()
                if column_name in untouched_columns_set
            }
            writer.writerow(sliced_row)

    __call__ = anonymize_file
