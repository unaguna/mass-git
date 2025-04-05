import typing as t

from ._cmn import SubCmd
from ..res_processor import StdoutDefault


class CheckoutCmd(SubCmd):
    def name(self) -> str:
        return "checkout"

    def help(self) -> str:
        return "Switch branches or restore working tree files"

    def subprocess_result_processor(self, args: t.Sequence[str]):
        return StdoutDefault()
