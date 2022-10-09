import click


@click.group()
def cli():
    pass

@cli.command()
def hello():
    click.echo('Hello there')


if __name__ == '__main__':
    cli()
