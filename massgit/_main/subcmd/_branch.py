import typing as t

from ._cmn import SubCmd
from ..stdout_type import StdoutDefault


class BranchCmd(SubCmd):
    def name(self) -> str:
        return "branch"

    def help(self) -> str:
        return "List, create, or delete branches"

    def stdout_type(self, args: t.Sequence[str]):
        return StdoutDefault()
