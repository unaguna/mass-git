import shutil
import sys
from pathlib import Path
import typing as t
from pprint import pprint

import yaml


class _DefMockSubprocRepoTypedDict(t.TypedDict):
    dirname: str
    markers: t.Optional[t.Sequence[str]]


class _DefMockSubprocRaiseTypedDict(t.TypedDict):
    msg: str


class _DefMockSubprocMockTypedDict(t.TypedDict):
    repo: _DefMockSubprocRepoTypedDict
    expected_cmd: t.Sequence[str]
    result_code: int
    stdout: str
    stderr: t.Optional[str]
    exception: t.Optional[_DefMockSubprocRaiseTypedDict]


class _DefMockSubprocTypedDict(t.TypedDict):
    input_args: t.Sequence[str]
    mock: t.Sequence[_DefMockSubprocMockTypedDict]
    expected_result_code: t.Optional[int]
    expected_stdout: t.Optional[str]
    expected_stderr: t.Optional[str]


def _do_nothing(_: t.Any):
    pass


def _create_mock_callback(
    mock: _DefMockSubprocMockTypedDict,
    *,
    trap_stderr: bool,
) -> t.Callable:
    stderr = mock.get("stderr")
    exception = mock.get("exception")

    def _mock_callback(_: t.Any):
        if not trap_stderr and stderr is not None:
            print(stderr, file=sys.stderr, end="")

        if exception is not None:
            raise Exception(exception.get("msg") or "exception for test")

    return _mock_callback


class DefMockSubproc:
    _base_dict: _DefMockSubprocTypedDict

    def __init__(self, base_dict: _DefMockSubprocTypedDict):
        self._base_dict = base_dict

    def pprint(self):
        pprint(self._base_dict)

    def mock_param_iter(
        self,
        *,
        trap_stderr: bool = False,
    ) -> t.Iterable[t.Dict[str, t.Any]]:
        """FakeProcess.registerの引数として使用する辞書をイテレーションする。

        Parameters
        ----------
        trap_stderr
            True の場合、サブプロセス実行時に標準エラー出力が PIPE 等で取得されることを前提にモック化する。
            False の場合、サブプロセス実行時に標準エラー出力がそのまま標準エラー出力へ出力されることを前提にモック化する。
        """
        for mock in self._base_dict["mock"]:
            command = mock["expected_cmd"]
            if command is None:
                continue

            yield {
                "command": command,
                "returncode": mock["result_code"],
                "stdout": mock["stdout"],
                "stderr": mock["stderr"] if trap_stderr else None,
                "callback": _create_mock_callback(mock, trap_stderr=trap_stderr),
            }

    def repos(self) -> t.Sequence[_DefMockSubprocRepoTypedDict]:
        return [m["repo"] for m in self._base_dict["mock"]]

    @property
    def input_args(self) -> t.Sequence[str]:
        return self._base_dict["input_args"]

    @property
    def expected_result_code(self) -> int:
        stored = self._base_dict.get("expected_result_code")
        return stored if stored is not None else NotSpecified()

    @property
    def expected_stdout(self) -> str:
        stored = self._base_dict["expected_stdout"]
        return stored if stored is not None else NotSpecified()

    @property
    def expected_stderr(self) -> str:
        stored = self._base_dict["expected_stderr"]
        return stored if stored is not None else NotSpecified()


class TestResources:
    _basedir: Path
    _tmp_path: Path
    _use_file_count: int

    def __init__(self, basedir: Path, *, tmp_path: Path):
        self._basedir = basedir
        self._tmp_path = tmp_path
        self._use_file_count = 0

        if not self._basedir.is_dir():
            raise FileNotFoundError(self._basedir)

    def use_file(self, relative_path: str) -> Path:
        src_path = self._basedir.joinpath(relative_path)
        use_file_dest = self._tmp_path.joinpath("use_file_dest")
        dest_path = use_file_dest.joinpath(str(self._use_file_count))

        if not use_file_dest.is_dir():
            use_file_dest.mkdir()

        return shutil.copyfile(src_path, dest_path)

    def load_mock_subproc(self, name: str) -> DefMockSubproc:
        with open(self._basedir.joinpath("def_mock_subprocess", name + ".yaml")) as fp:
            d: _DefMockSubprocTypedDict = yaml.safe_load(fp)

        return DefMockSubproc(d)


class NotSpecified:
    def __eq__(self, other):
        return True
