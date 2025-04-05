import typing as t

from ._cmn import SubCmd
from ..stdout_type import StdoutOnlyResultMessage


class CloneCmd(SubCmd):
    def name(self) -> str:
        return "clone"

    def help(self) -> str:
        return "Clone repositories into new directories"

    def stdout_type(self, args: t.Sequence[str]):
        return StdoutOnlyResultMessage()
