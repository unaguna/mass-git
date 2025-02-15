import argparse
import typing as t


class Params:
    _args: argparse.Namespace

    def __init__(self, args: argparse.Namespace):
        self._args = args

    @property
    def repos_file(self) -> str:
        return "repos.json"

    @property
    def basedir(self) -> t.Optional[str]:
        return None
