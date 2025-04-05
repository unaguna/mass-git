import typing as t

from ._cmn import SubCmd
from ..stdout_type import StdoutDefault


class CheckoutCmd(SubCmd):
    def name(self) -> str:
        return "checkout"

    def help(self) -> str:
        return "Switch branches or restore working tree files"

    def stdout_type(self, args: t.Sequence[str]):
        return StdoutDefault()
