import typing as t
from collections import defaultdict

from pytest_subprocess import FakeProcess

from ..resources import DefMockSubproc


def mock_subproc(
    def_mock_subproc: DefMockSubproc,
    *,
    fp: FakeProcess,
    trap_stderr: bool = False,
):
    calls = []
    for mock_kwargs in def_mock_subproc.mock_param_iter(trap_stderr=trap_stderr):
        fp.register(**mock_kwargs)
        calls.append(ExpectedCall(mock_kwargs["command"], 1))

    return MockedSubproc(fp=fp, calls=calls)


class ExpectedCall(t.NamedTuple):
    command: t.Sequence[str]
    count: int


class MockedSubproc:
    _fp: FakeProcess
    _calls: t.Sequence[ExpectedCall]

    def __init__(self, fp: FakeProcess, calls: t.Sequence[ExpectedCall]):
        self._fp = fp
        self._calls = calls

    def assert_call_count(self) -> t.Literal[True]:
        """モック化した subprocess の呼び出し回数を assert する。

        利用側で assert としてハイライトさせることを目的に
        `assert obj.assert_call_count()` と書くことができるようにするために、
        AssertionError 発生時以外は True を返す。
        """
        for cmd, count in self.expected_calls():
            assert self._fp.call_count(cmd) == count

        return True

    def expected_calls(self) -> t.Iterator[ExpectedCall]:
        # まず重複する指定を集計する
        buf: t.Mapping[t.Tuple[str, ...], int] = defaultdict(int)
        for call in self._calls:
            buf[tuple(call.command)] += call.count

        for command, count in buf.items():
            yield ExpectedCall(command, count)
