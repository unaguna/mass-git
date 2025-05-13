import os
import sys
import typing as t

from ._cmn import SubCmd
from ..res_processor import StdoutNameEachLinePrefix, SubprocessResultProcessor


class GrepCmd(SubCmd):
    def name(self) -> str:
        return "grep"

    def help(self) -> str:
        return "Print lines matching a pattern"

    def subprocess_result_processor(
        self, args: t.Sequence[str], *, rep_suffix: t.Optional[str]
    ) -> SubprocessResultProcessor:
        stdout_line_sep = "\0" if "-z" in args or "--null" in args else "\n"

        return StdoutNameEachLinePrefix(
            sep=rep_suffix if rep_suffix is not None else os.sep,
            trim_empty_line=True,
            result_line_sep=stdout_line_sep,
            output_line_sep=stdout_line_sep,
        )

    def exit_code_is_no_error(self, exit_code: int) -> bool:
        return exit_code == 0 or exit_code == 1

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
