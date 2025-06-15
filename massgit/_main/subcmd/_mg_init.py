import argparse
import typing as t

from ._cmn import SubCmd


class MgInitCmd(SubCmd):
    def name(self) -> str:
        return "mg-init"

    def help(self) -> str:
        return "Initialize massgit"

    def validate(
        self,
        main_args: argparse.Namespace,
        sub_args: t.Optional[argparse.Namespace],
        subparser: argparse.ArgumentParser,
    ):
        if main_args.marker_condition is not None:
            subparser.error(
                f"argument --marker/-m: cannot specify marker in {self.name()}"
            )
