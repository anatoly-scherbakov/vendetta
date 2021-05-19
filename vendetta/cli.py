from pathlib import Path
from sys import stdout, stdin
from typing import Optional

import strictyaml
import typer

from vendetta.models import Config
from vendetta.vendetta import Vendetta

app = typer.Typer()


def read_config(path: Path) -> Config:
    """Read configuration file."""
    raw = path.read_text()
    parsed = strictyaml.load(raw).data
    return Config(**parsed)


@app.command()
def cli(
    config_file: Path,
    source: Optional[Path] = None,
    destination: Optional[Path] = None,
) -> None:
    """Vendetta: anonymize CSV datasets."""
    config = read_config(config_file)
    vendetta = Vendetta(
        config=config,
    )

    with source.open('r') if source else stdin as input_file:
        with destination.open('w') if destination else stdout as output_file:
            vendetta(
                input_file=input_file,
                output_file=output_file,
            )


def main() -> None:
    app()


if __name__ == '__main__':
    main()
