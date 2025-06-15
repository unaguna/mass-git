import typing as t

from ._cmn import WrapGitSubCmd
from ..res_processor import StdoutDefault


class BranchCmd(WrapGitSubCmd):
    def name(self) -> str:
        return "branch"

    def help(self) -> str:
        return "List, create, or delete branches"

    def subprocess_result_processor(
        self, args: t.Sequence[str], *, rep_suffix: t.Optional[str]
    ):
        return StdoutDefault(sep=rep_suffix)
