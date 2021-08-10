import pathlib

from nore.util import minimize_path


class TestMinimizePath:
    def test_minimize_path_no_match(self):
        test_path = pathlib.Path().home().parent
        assert minimize_path(test_path) == test_path

    def test_minimize_path_home(self):
        test_path = pathlib.Path.home()
        assert minimize_path(test_path) == pathlib.Path("~")

    def test_minimize_path_home_child(self):
        test_path = pathlib.Path.home() / "test"
        assert minimize_path(test_path) == pathlib.Path("~/test")

    def test_minimize_path_cwd(self):
        test_path = pathlib.Path.cwd()
        assert minimize_path(test_path) == pathlib.Path(".")

    def test_minimize_path_cwd_child(self):
        test_path = pathlib.Path.cwd() / "test"
        assert minimize_path(test_path) == pathlib.Path("./test")
