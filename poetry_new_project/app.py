import subprocess
from functools import wraps
from os import environ

import click


def error_guard(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            click.echo(click.style(f"Error: {e}", fg="red"))
            exit(1)

    return wrapper_func


@click.command()
@click.option(
    "--version", default="3.9.5", help="Python version for the virtual environment"
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Force creation of environment by deleting existing environments with the same name",
)
@click.argument("venv_name")
@error_guard
def cli(venv_name: str, version: str, force: bool):

    pyenv_exists = subprocess.run(f"pyenv --version", shell=True, capture_output=True)

    # error out if pyenv not installed
    if pyenv_exists.returncode != 0:
        click.echo(
            [
                click.style(
                    "Error: pyenv not installed. Please install pyenv before continuing.",
                    fg="red",
                ),
                click.style(
                    "See: https://github.com/pyenv/pyenv-installer for installation instructions.",
                    fg="white",
                ),
            ]
        )
        exit(1)

    if force:
        click.echo(
            click.style(
                f"Deleting existing virtual environment {venv_name}", fg="green"
            )
        )
        subprocess.run(
            f"yes | pyenv virtualenv-delete {venv_name}",
            shell=True,
            capture_output=True,
            executable="/bin/bash",
        )

    # try to create virtualenv
    # if the python version is not installed
    # then install and try again
    try:
        click.echo(
            click.style(f"Creating virtual environment {venv_name}...", fg="green")
        )
        subprocess.run(
            f"pyenv virtualenv {version} {venv_name}",
            shell=True,
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"Python version {version} not installed!", fg="red"))
        click.echo(click.style(f"Installing python version {version}...", fg="green"))

        # input 'N' is so that if a python version is already installed, we just skip re-installing it
        out = subprocess.run(
            f"pyenv install {version}",
            shell=True,
            capture_output=True,
            input=b"N",
        )

        try:
            subprocess.run(
                f"pyenv virtualenv {version} {venv_name}",
                shell=True,
                capture_output=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            click.echo(
                click.style(
                    f"Suggestion: If the environment has already been created, try using --force to recreate the environment.",
                    fg="yellow",
                )
            )
            raise e

    click.echo(click.style(f"Installing poetry in {venv_name}", fg="green"))
    subprocess.run(
        f"~/.pyenv/versions/{venv_name}/bin/python -m pip install poetry",
        shell=True,
        capture_output=False,
        check=True,
        executable="/bin/bash",
    )

    click.echo(click.style(f"Running poetry init...", fg="green"))
    subprocess.run(
        f"poetry init",
        shell=True,
        capture_output=False,
        check=True,
        executable="/bin/bash",
    )

    click.echo(
        "".join(
            [
                f"Created virtual environment ",
                click.style(venv_name, fg="green"),
                " with python version ",
                click.style(version, fg="green"),
            ]
        )
    )

    click.echo(
        "".join(
            [
                "Activate virtual environment by running: ",
                click.style(
                    f"pyenv shell {venv_name}",
                    fg="green",
                ),
            ]
        )
    )


if __name__ == "__main__":
    cli()
