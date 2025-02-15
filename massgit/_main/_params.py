import argparse
import typing as t

from ._env_name import EnvKey


class Params:
    _args: argparse.Namespace
    _env: t.Dict[str, str]

    def __init__(self, args: argparse.Namespace, env: t.Dict[str, str]):
        self._args = args
        self._env = env

    @property
    def repos_file(self) -> str:
        if EnvKey.REPOS_FILE in self._env:
            return self._env[EnvKey.REPOS_FILE]
        return "repos.json"

    @property
    def basedir(self) -> t.Optional[str]:
        return None
