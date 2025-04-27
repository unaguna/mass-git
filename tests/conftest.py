import os
import typing as t
from pathlib import Path

import pytest
from pytest_subprocess import FakeProcess

from tests.utils.mock import mock_subproc
from tests.utils.output_detail import OutputDetail
from tests.utils.resources import TestResources


@pytest.fixture
def mock_sep(monkeypatch, tmp_path) -> t.Iterator[str]:
    """mock os.sep for multi-platform test"""

    sep = "/"
    origin_sep = os.sep
    os.sep = sep
    yield sep
    os.sep = origin_sep


@pytest.fixture
def mock_subprocess(fp: FakeProcess):
    """the function to mock subprocess.Open and .run by pytest-subprocess according the definition"""

    return lambda *args, **kwargs: mock_subproc(*args, **kwargs, fp=fp)


@pytest.fixture
def tmp_cwd(monkeypatch, tmp_path) -> Path:
    """change working directory temporary"""

    pwd = tmp_path.joinpath("working")
    pwd.mkdir()
    monkeypatch.chdir(pwd)
    return pwd


@pytest.fixture
def tmp_config_dir(monkeypatch, tmp_path) -> Path:
    """create install_config_dir"""

    env_dir = tmp_path.joinpath("env_dir")
    env_dir.mkdir()
    return env_dir


@pytest.fixture
def resources() -> TestResources:
    """Accessor to test resources"""
    return TestResources(Path(os.path.dirname(__file__), "resources"))


@pytest.fixture(scope="session")
def output_detail() -> OutputDetail:
    """the object to print details of pytest into stdout"""
    return OutputDetail()
