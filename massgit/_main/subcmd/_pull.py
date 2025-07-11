import typing as t

from ._cmn import WrapGitSubCmd
from ..res_processor import StdoutDefault


class PullCmd(WrapGitSubCmd):
    def name(self) -> str:
        return "pull"

    def help(self) -> str:
        return "Fetch from and integrate with another repository or a local branch"

    def subprocess_result_processor(
        self, args: t.Sequence[str], *, rep_suffix: t.Optional[str]
    ):
        return StdoutDefault(sep=rep_suffix)
