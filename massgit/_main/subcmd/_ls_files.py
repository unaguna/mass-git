import os
import sys
import typing as t

from ._cmn import SubCmd
from ..res_processor import (
    StdoutNameEachLinePrefix,
    SubprocessResultProcessor,
)


class LsFillsCmd(SubCmd):
    def name(self) -> str:
        return "ls-files"

    def help(self) -> str:
        return "Show information about files in the index and the working tree"

    def subprocess_result_processor(
        self, args: t.Sequence[str], *, rep_suffix: t.Optional[str]
    ) -> SubprocessResultProcessor:
        return StdoutNameEachLinePrefix(
            sep=rep_suffix if rep_suffix is not None else os.sep, trim_empty_line=True
        )

    def file_to_output_fail_msg(self, args: t.Sequence[str]) -> t.TextIO:
        return sys.stderr
