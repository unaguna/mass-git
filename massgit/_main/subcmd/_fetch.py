import typing as t

from ._cmn import SubCmd
from ..res_processor import StdoutDefault


class FetchCmd(SubCmd):
    def name(self) -> str:
        return "fetch"

    def help(self) -> str:
        return "Download objects and refs from another repository"

    def subprocess_result_processor(
        self, args: t.Sequence[str], *, rep_suffix: t.Optional[str]
    ):
        return StdoutDefault(sep=rep_suffix)
