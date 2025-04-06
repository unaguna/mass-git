import os
import typing as t
from pathlib import Path

import pytest
from pytest_subprocess import FakeProcess

from tests.utils.output_detail import OutputDetail
from tests.utils.resources import TestResources, DefMockSubproc


@pytest.fixture
def mock_sep(monkeypatch, tmp_path) -> t.Iterator[str]:
    sep = "/"
    origin_sep = os.sep
    os.sep = sep
    yield sep
    os.sep = origin_sep


@pytest.fixture
def mock_subprocess(fp: FakeProcess) -> t.Callable[[DefMockSubproc], None]:
    def _mock_subproc(def_mock_subproc: DefMockSubproc):
        for mock_kwargs in def_mock_subproc.mock_param_iter():
            fp.register(**mock_kwargs)

    return _mock_subproc


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
