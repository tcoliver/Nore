import pathlib
from typing import List, Optional
from urllib.error import URLError
from urllib.request import urlopen

import click
import pydantic


class FileInfo(pydantic.BaseModel):
    filename: str = pydantic.Field(..., alias="name")
    url: pydantic.HttpUrl
    download_url: Optional[pydantic.HttpUrl] = None
    size: int = pydantic.Field(..., ge=0)
    type: str

    class Config:
        allow_mutation = False
        allow_population_by_field_name = True


class IgnoreFileInfo(FileInfo):
    download_url = pydantic.HttpUrl

    @pydantic.validator("filename")
    def must_end_with_gitingore(cls, v):
        if not v.endswith(".gitignore"):
            raise ValueError("The filename must end with '.gitignore'")
        return v

    @classmethod
    def from_file_info(cls, model: FileInfo):
        return IgnoreFileInfo(**model.dict())

    @property
    def environment(self) -> str:
        return self.filename.removesuffix(".gitignore").lower()


def minimize_path(path: pathlib.Path) -> pathlib.Path:
    if path.is_relative_to(pathlib.Path.cwd()):
        return "." / path.relative_to(pathlib.Path.cwd())
    elif path.is_relative_to(pathlib.Path.home()):
        return "~" / path.relative_to(pathlib.Path.home())
    else:
        return path


def get_environment_file_list() -> List[IgnoreFileInfo]:
    gitignore_url = "https://api.github.com/repos/github/gitignore/contents/"
    try:
        with urlopen(gitignore_url) as response:
            if response.status != 200:
                click.secho(
                    f"Unable to open {response.url} ({response.status})",
                    fg="red",
                    err=True,
                )
                raise click.Abort()
            file_list: List[FileInfo] = pydantic.parse_raw_as(
                List[FileInfo], response.read()
            )
    except URLError as e:
        click.secho(
            f"Error: Unable to contact {gitignore_url}", fg="red", err=True
        )
        click.secho(f"       {e.reason}", fg="red", err=True)
        raise click.Abort()
    except pydantic.ValidationError as e:
        click.secho(
            f"Unable to parse response from {gitignore_url}\n\n{e}",
            fg="red",
            err=True,
        )
        raise click.Abort()

    return list(
        map(
            IgnoreFileInfo.from_file_info,
            filter(
                lambda x: x.type == "file"
                and x.filename.endswith(".gitignore"),
                file_list,
            ),
        )
    )
