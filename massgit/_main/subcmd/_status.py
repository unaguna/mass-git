import typing as t

from ._cmn import WrapGitSubCmd
from ..res_processor import (
    StdoutDefault,
    StdoutNameEachLinePrefix,
    SubprocessResultProcessor,
)


class StatusCmd(WrapGitSubCmd):
    def name(self) -> str:
        return "status"

    def help(self) -> str:
        return "Show the working tree status"

    def subprocess_result_processor(
        self, args: t.Sequence[str], *, rep_suffix: t.Optional[str]
    ) -> SubprocessResultProcessor:
        porcelain = "--porcelain" in ",".join(args)

        if porcelain:
            return StdoutNameEachLinePrefix(sep=rep_suffix, trim_empty_line=True)
        else:
            return StdoutDefault(sep=rep_suffix)
