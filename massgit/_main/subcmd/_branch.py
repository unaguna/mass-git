import typing as t

from ._cmn import SubCmd
from ..res_processor import StdoutDefault


class BranchCmd(SubCmd):
    def name(self) -> str:
        return "branch"

    def help(self) -> str:
        return "List, create, or delete branches"

    def subprocess_result_processor(self, args: t.Sequence[str]):
        return StdoutDefault()
