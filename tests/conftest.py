import pytest


@pytest.fixture
def tmp_cwd(monkeypatch, tmp_path):
    pwd = tmp_path.joinpath("working")
    pwd.mkdir()
    monkeypatch.chdir(pwd)
    return pwd
