import os
import typing as t

from ._cmn import SubCmd
from ..res_processor import (
    StdoutDefault,
    StdoutNameEachLinePrefix,
    SubprocessResultProcessor,
)


class DiffCmd(SubCmd):
    def name(self) -> str:
        return "diff"

    def help(self) -> str:
        return "Show changes between commits, commit and working tree, etc"

    def subprocess_result_processor(
        self, args: t.Sequence[str], *, rep_suffix: t.Optional[str]
    ) -> SubprocessResultProcessor:
        joined_args = " ".join(args)
        shortstat = "--shortstat" in joined_args
        name_only = "--name-only" in joined_args

        if shortstat:
            return StdoutDefault(
                output_with_empty_stdout="0 file changed", sep=rep_suffix
            )
        elif name_only:
            return StdoutNameEachLinePrefix(
                sep=rep_suffix if rep_suffix is not None else os.sep,
                trim_empty_line=True,
            )
        else:
            return StdoutDefault(output_with_empty_stdout="no diffs", sep=rep_suffix)
