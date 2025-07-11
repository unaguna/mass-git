import json
import os
import typing as t
from pathlib import PurePath


class _EmptySet:
    def __contains__(self, item):
        return False


def _repo(repo: t.Mapping, *, no_url_dirnames: t.Set[str]) -> t.Dict[str, t.Any]:
    repo = {"url": f"http://example.com/{repo['dirname']}", **repo}

    if repo["dirname"] in no_url_dirnames:
        del repo["url"]

    return repo


class MassgitDir:
    _massgit_dir_path: os.PathLike[str]
    _repos_path: os.PathLike[str]

    def __init__(
        self, massgit_dir_path: os.PathLike[str], repos_path: os.PathLike[str]
    ):
        self._massgit_dir_path = massgit_dir_path
        self._repos_path = repos_path

    @property
    def massgit_dir_path(self) -> os.PathLike[str]:
        return self._massgit_dir_path

    @property
    def repos_path(self) -> os.PathLike[str]:
        return self._repos_path

    def log_conf_path(self, exp: t.Literal["yaml", "json"] = "yaml") -> str:
        return os.path.join(self.massgit_dir_path, f"logging_conf.{exp}")


def create_massgit_dir(
    cwd: os.PathLike,
    repos: t.Sequence = ({"dirname": "repo1"},),
    *,
    repos_path: t.Union[os.PathLike[str], str, None] = None,
    no_url_dirnames: t.Set[str] = _EmptySet(),
) -> MassgitDir:
    if repos_path is None:
        repos_path = PurePath(cwd, ".massgit", "repos.json")
    elif isinstance(repos_path, str):
        repos_path = PurePath(repos_path)
    massgit_dir_path = repos_path.parent
    os.mkdir(massgit_dir_path)

    repos = [_repo(repo, no_url_dirnames=no_url_dirnames) for repo in repos]

    with open(repos_path, mode="w") as fp:
        json.dump(repos, fp)

    return MassgitDir(
        massgit_dir_path=massgit_dir_path,
        repos_path=repos_path,
    )
