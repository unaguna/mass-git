import os
import typing as t
from pathlib import Path

import pytest

from tests.utils.output_detail import OutputDetail
from tests.utils.resources import TestResources


@pytest.fixture
def mock_sep(monkeypatch, tmp_path) -> t.Iterator[str]:
    sep = "/"
    origin_sep = os.sep
    os.sep = sep
    yield sep
    os.sep = origin_sep


@pytest.fixture
def tmp_cwd(monkeypatch, tmp_path) -> Path:
    pwd = tmp_path.joinpath("working")
    pwd.mkdir()
    monkeypatch.chdir(pwd)
    return pwd


@pytest.fixture
def resources() -> TestResources:
    return TestResources(Path(os.path.dirname(__file__), "resources"))


@pytest.fixture(scope="session")
def output_detail() -> OutputDetail:
    return OutputDetail()
