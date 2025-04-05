import os
import typing as t

from ._cmn import SubCmd
from ..stdout_type import StdoutDefault, StdoutNameEachLinePrefix, StdoutType


class DiffCmd(SubCmd):
    def name(self) -> str:
        return "diff"

    def help(self) -> str:
        return "Show changes between commits, commit and working tree, etc"

    def stdout_type(self, args: t.Sequence[str]) -> StdoutType:
        joined_args = " ".join(args)
        shortstat = "--shortstat" in joined_args
        name_only = "--name-only" in joined_args

        if shortstat:
            return StdoutDefault(output_with_empty_stdout="0 file changed")
        elif name_only:
            return StdoutNameEachLinePrefix(sep=os.sep, trim_empty_line=True)
        else:
            return StdoutDefault(output_with_empty_stdout="no diffs")
