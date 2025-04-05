import typing as t

from ._cmn import SubCmd
from ..stdout_type import StdoutDefault


class FetchCmd(SubCmd):
    def name(self) -> str:
        return "fetch"

    def help(self) -> str:
        return "Download objects and refs from another repository"

    def stdout_type(self, args: t.Sequence[str]):
        return StdoutDefault()
