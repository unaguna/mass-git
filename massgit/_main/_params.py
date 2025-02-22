import argparse
import os
import typing as t

from ._env_name import EnvKey


class Params:
    _args: argparse.Namespace
    _sub_args: t.Optional[argparse.Namespace]
    _remaining_args: t.Sequence[str]
    _env: t.Dict[str, str]
    _cwd_config_dir: t.Union[str, os.PathLike]

    def __init__(
        self,
        args: argparse.Namespace,
        sub_args: t.Optional[argparse.Namespace],
        remaining_args: t.Sequence[str],
        env: t.Dict[str, str],
        cwd_config_dir: t.Union[str, os.PathLike],
    ):
        self._args = args
        self._sub_args = sub_args
        self._remaining_args = remaining_args
        self._env = env
        self._cwd_config_dir = cwd_config_dir

    @property
    def env(self) -> t.Dict[str, str]:
        return self._env

    @property
    def remaining_args(self) -> t.Sequence[str]:
        return self._remaining_args

    @property
    def massgit_dir(self) -> str:
        return self._cwd_config_dir

    @property
    def repos_file(self) -> str:
        if EnvKey.REPOS_FILE in self._env:
            return self._env[EnvKey.REPOS_FILE]
        return os.path.join(self.massgit_dir, "repos.json")

    @property
    def git_exec_path(self) -> str:
        if EnvKey.GIT_PATH in self._env:
            return self._env[EnvKey.GIT_PATH]
        return "git"

    @property
    def basedir(self) -> t.Optional[str]:
        return None

    @property
    def is_shortstat(self) -> bool:
        return getattr(self._args, "shortstat", False)

    @property
    def show_no_change(self) -> bool:
        return getattr(self._args, "show_no_change", False)

    @property
    def name_only(self) -> bool:
        return getattr(self._args, "name_only", False)
