import argparse
import os
import typing as t

from ._env_name import EnvKey
from .marker import MarkerProcessor, AcceptAnyMarkerProcessor


class Params:
    _args: argparse.Namespace
    _env: t.Dict[str, str]
    _cwd_config_dir: t.Union[str, os.PathLike]
    _marker_processor: MarkerProcessor

    def __init__(
        self,
        args: argparse.Namespace,
        env: t.Dict[str, str],
        cwd_config_dir: t.Union[str, os.PathLike],
    ):
        self._args = args
        self._env = env
        self._cwd_config_dir = cwd_config_dir

        self._marker_processor = (
            MarkerProcessor(
                self._args.marker_condition,
                ignore_case=not self._args.marker_case_sensitive,
            )
            if self._args.marker_condition is not None
            else AcceptAnyMarkerProcessor()
        )

    @property
    def env(self) -> t.Dict[str, str]:
        return self._env

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
    def rep_suffix(self) -> t.Optional[str]:
        return _or(self._args.rep_suffix, self._env.get(EnvKey.REP_SUFFIX))

    @property
    def marker_processor(self) -> MarkerProcessor:
        return self._marker_processor


def _or(*args):
    for arg in args:
        if arg is not None:
            return arg
    else:
        return None
