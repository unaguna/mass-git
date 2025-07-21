import abc
import sys
import typing as t


class SubprocessResultProcessor(abc.ABC):
    @abc.abstractmethod
    def print_stdout(self, exit_code: int, origin_stdout: bytes, dirname: str): ...


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

    def print_stdout(self, exit_code: int, origin_stdout: bytes, dirname: str):
        stdout_trimmed = origin_stdout.strip()
        if stdout_trimmed.count(b"\n") <= 0:
            print(
                dirname,
                self._sep,
                sep="",
                end="",
            )
            if stdout_trimmed:
                sys.stdout.buffer.write(stdout_trimmed)
                print()
            else:
                print(self._output_with_empty_stdout)
        else:
            print(dirname + self._sep.rstrip())
            sys.stdout.buffer.write(origin_stdout)
            print()


class StdoutNameEachLinePrefix(SubprocessResultProcessor):
    _sep: str
    _trim_empty_line: bool
    _result_line_sep: bytes
    _output_line_sep: str

    def __init__(
        self,
        *,
        sep: t.Optional[str],
        trim_empty_line: bool = False,
        result_line_sep: t.Union[bytes, str] = b"\n",
        output_line_sep: str = "\n",
        output_encoding: str = sys.getdefaultencoding(),
    ):
        self._sep = sep if sep is not None else ": "
        self._trim_empty_line = trim_empty_line
        if isinstance(result_line_sep, str):
            result_line_sep = result_line_sep.encode(encoding=output_encoding)
        self._result_line_sep = result_line_sep
        self._output_line_sep = output_line_sep

    @property
    def separator(self) -> str:
        return self._sep

    def _line_iter(self, text: bytes) -> t.Iterator[bytes]:
        if self._trim_empty_line:
            for line in text.split(self._result_line_sep):
                if len(line) > 0:
                    yield line
        else:
            for line in text.split(self._result_line_sep):
                yield line

    def print_stdout(self, exit_code: int, origin_stdout: bytes, dirname: str):
        for line in self._line_iter(origin_stdout):
            print(dirname, self._sep, sep="", end="")
            sys.stdout.buffer.write(line)
            print(self._output_line_sep, end="")
