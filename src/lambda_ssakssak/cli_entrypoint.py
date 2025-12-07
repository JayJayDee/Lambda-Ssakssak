import click
from typing_extensions import Literal

_Mode = Literal['dry-run', 'execute']
all_modes: list[_Mode] = ['dry-run', 'execute']

@click.command()
@click.argument(
    'mode',
    type=click.Choice(all_modes, case_sensitive=False)
)
def main(mode: _Mode):
    """
    Lambda-SsakSsak: A tiny tool for cleaning up old AWS lambda versions.
    """
    click.echo(f"HOLA, {mode}")

if __name__ == "__main__":
    main()