import typing as t

from ._cmn import SubCmd
from ..res_processor import (
    StdoutDefault,
    StdoutNameEachLinePrefix,
    SubprocessResultProcessor,
)


class StatusCmd(SubCmd):
    def name(self) -> str:
        return "status"

    def help(self) -> str:
        return "Show the working tree status"

    def subprocess_result_processor(
        self, args: t.Sequence[str]
    ) -> SubprocessResultProcessor:
        porcelain = "--porcelain" in ",".join(args)

        if porcelain:
            return StdoutNameEachLinePrefix(sep=": ", trim_empty_line=True)
        else:
            return StdoutDefault()
