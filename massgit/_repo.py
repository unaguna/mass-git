import json
import os
import typing as t

from ._types import Repo


def load_repos(
    repos_file: t.Union[str, os.PathLike] = "repos.json",
) -> t.Sequence[Repo]:
    with open(repos_file, mode="r", encoding="utf-8") as fp:
        return json.load(fp)


def repo_dirname(repo: Repo) -> str:
    if "dirname" in repo:
        return repo["dirname"]
    else:
        return repo["url"].removesuffix(".git").rsplit("/", 2)[-1]
