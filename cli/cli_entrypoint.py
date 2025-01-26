import click

@click.command()
@click.argument('mode')
def main(mode: str):
    """
    Lambda-SsakSsak: A tiny tool for safely cleaning up old AWS lambda versions.
    """
    click.echo(f"Hello, {mode}")

if __name__ == "__main__":
    main()