import click
from typing_extensions import Literal
from lambda_ssakssak import aws_factory
from lambda_ssakssak.cleaner import run_cleaner
from lambda_ssakssak.context import get_ctx

_Mode = Literal['dry-run', 'execute']
all_modes: list[_Mode] = ['dry-run', 'execute']

@click.command()
@click.argument(
    'mode',
    type=click.Choice(all_modes, case_sensitive=False)
)
@click.option('--region', required=True, help='AWS region. e.g. ap-northeast-2')
@click.option('--keep', default=1, show_default=True, type=click.IntRange(min=0),
              help='Number of most recent published versions to retain per function.')
@click.option('--threads', default=5, show_default=True, type=click.IntRange(min=1),
              help='Number of threads for reading versions.')
def main(mode: str, region: str, keep: int, threads: int):
    """
    Lambda-SsakSsak: A tiny tool for cleaning up old AWS lambda versions.

    MODE: 'dry-run' only lists versions to be deleted, 'execute' deletes them.
    """
    get_ctx().put(aws_region=region)
    run_cleaner(
        client=aws_factory.lambda_(region),
        dry_run=(mode.lower() == 'dry-run'),
        keep=keep,
        num_threads=threads,
    )

if __name__ == "__main__":
    main()
