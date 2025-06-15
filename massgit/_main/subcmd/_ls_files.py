import os
import sys
import typing as t

from ._cmn import WrapGitSubCmd
from ..res_processor import (
    StdoutNameEachLinePrefix,
    SubprocessResultProcessor,
)


class LsFillsCmd(WrapGitSubCmd):
    def name(self) -> str:
        return "ls-files"

    def help(self) -> str:
        return "Show information about files in the index and the working tree"

    def subprocess_result_processor(
        self, args: t.Sequence[str], *, rep_suffix: t.Optional[str]
    ) -> SubprocessResultProcessor:
        stdout_line_sep = "\0" if "-z" in args else "\n"

        return StdoutNameEachLinePrefix(
            sep=rep_suffix if rep_suffix is not None else os.sep,
            trim_empty_line=True,
            result_line_sep=stdout_line_sep,
            output_line_sep=stdout_line_sep,
        )

    def file_to_output_fail_msg(self, args: t.Sequence[str]) -> t.TextIO:
        return sys.stderr
