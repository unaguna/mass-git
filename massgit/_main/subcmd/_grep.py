import os
import sys
import typing as t

from ._cmn import SubCmd
from ..stdout_type import StdoutNameEachLinePrefix, StdoutType


class GrepCmd(SubCmd):
    def name(self) -> str:
        return "grep"

    def help(self) -> str:
        return "Print lines matching a pattern"

    def stdout_type(self, args: t.Sequence[str]) -> StdoutType:
        return StdoutNameEachLinePrefix(sep=os.sep, trim_empty_line=True)

    def file_to_output_fail_msg(self, args: t.Sequence[str]) -> t.TextIO:
        return sys.stderr

    def summarize_exit_code(self, exit_codes: t.Iterable[int]) -> int:
        exit_codes_list = list(exit_codes)
        exit_codes_err = [c for c in exit_codes_list if c not in (0, 1)]

        if len(exit_codes_err) > 0:
            return max(exit_codes_err)
        elif 0 in exit_codes_list:
            return 0
        else:
            return 1
