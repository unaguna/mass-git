import os
from pathlib import Path

import pytest

from tests.utils.resources import TestResources


@pytest.fixture
def tmp_cwd(monkeypatch, tmp_path) -> Path:
    pwd = tmp_path.joinpath("working")
    pwd.mkdir()
    monkeypatch.chdir(pwd)
    return pwd


@pytest.fixture
def resources() -> TestResources:
    return TestResources(Path(os.path.dirname(__file__), "resources"))
