import argparse
import typing as t

from ._env_name import EnvKey


class Params:
    _args: argparse.Namespace
    _sub_args: t.Optional[argparse.Namespace]
    _remaining_args: t.Sequence[str]
    _env: t.Dict[str, str]

    def __init__(
        self,
        args: argparse.Namespace,
        sub_args: t.Optional[argparse.Namespace],
        remaining_args: t.Sequence[str],
        env: t.Dict[str, str],
    ):
        self._args = args
        self._sub_args = sub_args
        self._remaining_args = remaining_args
        self._env = env

    @property
    def remaining_args(self) -> t.Sequence[str]:
        return self._remaining_args

    @property
    def repos_file(self) -> str:
        if EnvKey.REPOS_FILE in self._env:
            return self._env[EnvKey.REPOS_FILE]
        return "repos.json"

    @property
    def basedir(self) -> t.Optional[str]:
        return None

    @property
    def is_shortstat(self) -> bool:
        return getattr(self._args, "shortstat", False)
