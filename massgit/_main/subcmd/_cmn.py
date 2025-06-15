import abc
import itertools
import sys
import typing as t

from ..res_processor import SubprocessResultProcessor


class SubCmd(abc.ABC):
    @abc.abstractmethod
    def name(self) -> str: ...

    @abc.abstractmethod
    def help(self) -> t.Optional[str]: ...

    def parse_sub_args(self) -> bool:
        return True


class WrapGitSubCmd(SubCmd, abc.ABC):
    def parse_sub_args(self) -> bool:
        return False

    @abc.abstractmethod
    def subprocess_result_processor(
        self, args: t.Sequence[str], *, rep_suffix: t.Optional[str]
    ) -> SubprocessResultProcessor: ...

    def exit_code_is_no_error(self, exit_code: int) -> bool:
        """judge which the exit_code of git command means non-error"""
        return exit_code == 0

    def file_to_output_fail_msg(self, args: t.Sequence[str]) -> t.TextIO:
        return sys.stdout

    def summarize_exit_code(self, exit_codes: t.Iterable[int]) -> int:
        return max(itertools.chain(exit_codes, (0,)))
