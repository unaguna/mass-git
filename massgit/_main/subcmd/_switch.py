import typing as t

from ._cmn import WrapGitSubCmd
from ..res_processor import StdoutDefault


class SwitchCmd(WrapGitSubCmd):
    def name(self) -> str:
        return "switch"

    def help(self) -> str:
        return "Switch branches"

    def subprocess_result_processor(
        self, args: t.Sequence[str], *, rep_suffix: t.Optional[str]
    ):
        return StdoutDefault(sep=rep_suffix)
