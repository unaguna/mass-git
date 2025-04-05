import typing as t

from ._cmn import SubCmd
from ..res_processor import StdoutDefault


class PullCmd(SubCmd):
    def name(self) -> str:
        return "pull"

    def help(self) -> str:
        return "Fetch from and integrate with another repository or a local branch"

    def subprocess_result_processor(self, args: t.Sequence[str]):
        return StdoutDefault()
