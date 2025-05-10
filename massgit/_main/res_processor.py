import abc
import typing as t


class SubprocessResultProcessor(abc.ABC):
    @abc.abstractmethod
    def print_stdout(self, exit_code: int, origin_stdout: str, dirname: str): ...


class StdoutDefault(SubprocessResultProcessor):
    _sep: str
    _output_with_empty_stdout: str

    def __init__(
        self, *, sep: t.Optional[str] = None, output_with_empty_stdout: str = "done"
    ):
        self._sep = sep if sep is not None else ": "
        self._output_with_empty_stdout = output_with_empty_stdout

    @property
    def separator(self) -> str:
        return self._sep

    def print_stdout(self, exit_code: int, origin_stdout: str, dirname: str):
        stdout_trimmed = origin_stdout.strip()
        if stdout_trimmed.count("\n") <= 0:
            print(
                dirname,
                self._sep,
                stdout_trimmed or self._output_with_empty_stdout,
                sep="",
            )
        else:
            print(dirname + self._sep.rstrip())
            print(origin_stdout)


class StdoutNameEachLinePrefix(SubprocessResultProcessor):
    _sep: str
    _trim_empty_line: bool

    def __init__(self, *, sep: t.Optional[str], trim_empty_line: bool = False):
        self._sep = sep if sep is not None else ": "
        self._trim_empty_line = trim_empty_line

    @property
    def separator(self) -> str:
        return self._sep

    def _line_iter(self, text: str) -> t.Iterator[str]:
        if self._trim_empty_line:
            for line in text.split("\n"):
                if len(line) > 0:
                    yield line
        else:
            for line in text.split("\n"):
                yield line

    def print_stdout(self, exit_code: int, origin_stdout: str, dirname: str):
        for line in self._line_iter(origin_stdout):
            print(dirname, self._sep, line, sep="")
