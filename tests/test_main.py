from click.testing import CliRunner

from nore import __version__
from nore.main import app


def test_version_option():
    # noinspection PyTypeChecker
    result = CliRunner().invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.output.endswith(f", version {__version__}\n")


class TestNewCommand:
    def test_no_argument(self):
        assert False

    def test_one_argument(self):
        assert False

    def test_multiple_argument(self):
        assert False

    def test_output_path(self):
        assert False
