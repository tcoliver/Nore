from click.testing import CliRunner

from nore.main import app
from nore import __version__


def test_show_version():
    result = CliRunner().invoke(app, ['--version'])
    assert result.exit_code == 0
    assert result.output == f'app, version {__version__}\n'
