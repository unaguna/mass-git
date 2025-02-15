import argparse
import typing as t


class Params:
    _args: argparse.Namespace
    _env: t.Dict[str, str]

    def __init__(self, args: argparse.Namespace, env: t.Dict[str, str]):
        self._args = args
        self._env = env

    @property
    def repos_file(self) -> str:
        if "MASSGIT_REPOS_FILE" in self._env:
            return self._env["MASSGIT_REPOS_FILE"]
        return "repos.json"

    @property
    def basedir(self) -> t.Optional[str]:
        return None
