import typing as t

from ._cmn import SubCmd
from ..res_processor import StdoutDefault


class ShowCmd(SubCmd):
    def name(self) -> str:
        return "show"

    def help(self) -> str:
        return "Show various types of objects"

    def subprocess_result_processor(self, args: t.Sequence[str]):
        return StdoutDefault()
