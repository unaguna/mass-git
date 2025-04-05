import typing as t

from ._cmn import SubCmd
from ..stdout_type import StdoutDefault, StdoutNameEachLinePrefix, StdoutType


class StatusCmd(SubCmd):
    def name(self) -> str:
        return "status"

    def help(self) -> str:
        return "Show the working tree status"

    def stdout_type(self, args: t.Sequence[str]) -> StdoutType:
        porcelain = "--porcelain" in ",".join(args)

        if porcelain:
            return StdoutNameEachLinePrefix(sep=": ", trim_empty_line=True)
        else:
            return StdoutDefault()
