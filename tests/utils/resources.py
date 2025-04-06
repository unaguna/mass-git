from pathlib import Path
import typing as t

import yaml


class _DefMockSubprocRepoTypedDict(t.TypedDict):
    dirname: str


class _DefMockSubprocMockTypedDict(t.TypedDict):
    repo: _DefMockSubprocRepoTypedDict
    expected_cmd: t.Sequence[str]
    stdout: str


class _DefMockSubprocTypedDict(t.TypedDict):
    mock: t.Sequence[_DefMockSubprocMockTypedDict]
    expected_stdout: t.Optional[str]


class DefMockSubproc:
    _base_dict: _DefMockSubprocTypedDict

    def __init__(self, base_dict: _DefMockSubprocTypedDict):
        self._base_dict = base_dict

    def mock_param_iter(self) -> t.Iterable[t.Dict[str, t.Any]]:
        """FakeProcess.registerの引数として使用する辞書をイテレーションする。"""
        for mock in self._base_dict["mock"]:
            yield {
                "command": mock["expected_cmd"],
                "stdout": mock["stdout"],
            }

    def repo_dirnames(self) -> t.Sequence[str]:
        return [m["repo"]["dirname"] for m in self._base_dict["mock"]]

    @property
    def expected_stdout(self) -> str:
        stored = self._base_dict["expected_stdout"]
        return stored or ""


class TestResources:
    _basedir: Path

    def __init__(self, basedir: Path):
        self._basedir = basedir

        if not self._basedir.is_dir():
            raise FileNotFoundError(self._basedir)

    def load_mock_subproc(self, name: str) -> DefMockSubproc:
        with open(self._basedir.joinpath("def_mock_subprocess", name + ".yaml")) as fp:
            d: _DefMockSubprocTypedDict = yaml.safe_load(fp)

        return DefMockSubproc(d)
