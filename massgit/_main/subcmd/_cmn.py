import abc
import sys
import typing as t

from ..stdout_type import StdoutType


class SubCmd(abc.ABC):
    @abc.abstractmethod
    def name(self) -> str: ...

    @abc.abstractmethod
    def help(self) -> t.Optional[str]: ...

    @abc.abstractmethod
    def stdout_type(self, args: t.Sequence[str]) -> StdoutType: ...

    def file_to_output_fail_msg(self, args: t.Sequence[str]) -> t.TextIO:
        return sys.stdout

    def summarize_exit_code(self, exit_codes: t.Iterable[int]) -> int:
        return max(exit_codes)
