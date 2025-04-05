import typing as t

from ._cmn import SubCmd
from ..res_processor import StdoutOnlyResultMessage


class CloneCmd(SubCmd):
    def name(self) -> str:
        return "clone"

    def help(self) -> str:
        return "Clone repositories into new directories"

    def subprocess_result_processor(self, args: t.Sequence[str]):
        return StdoutOnlyResultMessage()
