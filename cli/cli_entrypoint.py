import click

@click.command()
@click.option('--name', default='World', help='Name to greet.')
@click.option('--test', default='test', help='Name to greet.')
def main(name, test):
    """A simple CLI tool."""
    click.echo(f"Hello, {name}, {test}")

if __name__ == "__main__":
    main()