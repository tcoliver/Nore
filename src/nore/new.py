import pathlib
from urllib.error import URLError
from urllib.request import urlopen

import click

from .util import get_environment_file_list, minimize_path


def get_download_url(environment: str) -> str:
    language_file_list = get_environment_file_list()
    for language_file in language_file_list:
        if language_file.environment.lower() == environment.lower():
            return language_file.download_url
    click.secho(f"{environment} not found in available options")
    raise click.Abort()


def download_gitignore(
    environment: str,
    output_path: pathlib.Path,
    output_filename: str = ".gitignore",
):
    download_url = get_download_url(environment)
    try:
        with urlopen(download_url) as response, open(
            output_path / output_filename, "w"
        ) as file:
            if response.status == 200:
                content = response.read().decode("utf-8")
                file.write(content)
                click.secho(
                    f"Created .gitignore at {minimize_path(output_path / output_filename)}",
                    fg="green",
                )
            else:
                click.secho("Error: Unable to download content", fg="red", err=True)
                click.Abort()
    except URLError as e:
        click.secho(f"Error: Unable to contact {download_url}", fg="red", err=True)
        click.secho(e, fg="red", err=True)
        click.Abort()
    except OSError as e:
        click.secho(
            f"Error: Unable to write file at {output_path / output_filename}",
            fg="red",
            err=True,
        )
        click.secho(e, fg="red", err=True)
        click.Abort()
