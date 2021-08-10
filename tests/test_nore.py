import pathlib

import pytest
import tomlkit

from nore import __version__


@pytest.fixture
def pyproject_toml(request):
    pyproject_path = pathlib.Path(request.fspath).parent.parent / "pyproject.toml"
    with open(pyproject_path, "r") as file:
        pyproject_content = tomlkit.parse(file.read())
    return pyproject_content


def test_version(pyproject_toml):
    assert __version__ == pyproject_toml["tool"]["poetry"]["version"]
