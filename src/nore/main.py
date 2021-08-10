import pathlib

import click

from . import __version__ as app_version
from .list import print_environment_list
from .new import download_gitignore


@click.group()
@click.version_option(app_version)
def app():
    """
    Nore is a simple utility for managing .gitignore files.

    You can download the .gitignore for any environment listed in the main
    portion of the github/gitingore repository.
    """
    pass


@app.command(no_args_is_help=True)
@click.argument("environment")
@click.option(
    "--output-path",
    "-o",
    default=pathlib.Path.cwd(),
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True,
        path_type=pathlib.Path,
    ),
    help="Where to create the .gitignore file.",
)
def new(environment: str, output_path: pathlib.Path):
    """
    Create a new .gitignore file for the specified ENVIRONMENT.

    ENVIRONMENT specifies the type of .gitignore file. A list of
    all available types can get retrieved by running `nore list`.
    """
    download_gitignore(environment, output_path=output_path)


@app.command(name="list")
def _list():
    """
    List all available environments.

    Returns a list of environment identifiers from the main templates on the
    github/gitignore repository.
    """
    print_environment_list()


if __name__ == "__main__":
    app()
