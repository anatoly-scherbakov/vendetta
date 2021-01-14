import csv
from pathlib import Path

import typer
import yaml

from vendetta.models import Config
from vendetta.vendetta import Vendetta

try:  # noqa
    from yaml import CSafeDumper as SafeDumper  # noqa
    from yaml import CSafeLoader as SafeLoader  # noqa
except ImportError:
    from yaml import SafeDumper  # type: ignore   # noqa
    from yaml import SafeLoader  # type: ignore   # noqa


app = typer.Typer()


def read_config() -> Config:
    """Read configuration file."""
    with (Path(__file__).parent.parent / 'config.yaml').open() as config_file:
        return Config(**yaml.load(config_file, Loader=SafeLoader))


@app.command()
def cli() -> None:
    """CLI."""
    config = read_config()
    source_directory = Path(
        '...',
    )
    destination_directory = Path(
        '...',
    )

    vendetta = Vendetta(config=config)

    for source_path in source_directory.rglob('*'):
        destination_path = destination_directory / source_path.relative_to(
            source_directory,
        )
        with source_path.open() as source_file:
            reader = csv.DictReader(source_file)

            if not destination_path.parent.exists():
                destination_path.parent.mkdir(parents=True, exist_ok=True)

            with destination_path.open('w+') as destination_file:
                writer = csv.DictWriter(
                    destination_file,
                    fieldnames=reader.fieldnames,
                )
                writer.writeheader()

                for row in reader:
                    writer.writerow(
                        vendetta.anonymize_row(row),
                    )


def main() -> None:
    app()


if __name__ == '__main__':
    main()
