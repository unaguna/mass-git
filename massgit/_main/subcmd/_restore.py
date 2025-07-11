import typing as t

from ._cmn import WrapGitSubCmd
from ..res_processor import StdoutDefault


class RestoreCmd(WrapGitSubCmd):
    def name(self) -> str:
        return "restore"

    def help(self) -> str:
        return "Restore working tree files"

    def subprocess_result_processor(
        self, args: t.Sequence[str], *, rep_suffix: t.Optional[str]
    ):
        return StdoutDefault(sep=rep_suffix)
