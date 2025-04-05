import typing as t

from ._cmn import SubCmd
from ..stdout_type import StdoutDefault


class ConfigCmd(SubCmd):
    def name(self) -> str:
        return "config"

    def help(self) -> str:
        return "Get and set repository options"

    def stdout_type(self, args: t.Sequence[str]):
        return StdoutDefault()
