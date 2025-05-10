import typing as t

from ._cmn import SubCmd
from ..res_processor import StdoutDefault


class ConfigCmd(SubCmd):
    def name(self) -> str:
        return "config"

    def help(self) -> str:
        return "Get and set repository options"

    def subprocess_result_processor(
        self, args: t.Sequence[str], *, rep_suffix: t.Optional[str]
    ):
        return StdoutDefault(sep=rep_suffix)
