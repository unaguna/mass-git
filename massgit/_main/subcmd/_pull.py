import typing as t

from ._cmn import SubCmd
from ..stdout_type import StdoutDefault


class PullCmd(SubCmd):
    def name(self) -> str:
        return "pull"

    def help(self) -> str:
        return "Fetch from and integrate with another repository or a local branch"

    def stdout_type(self, args: t.Sequence[str]):
        return StdoutDefault()
