import json
import os
import typing as t

from ._types import Repo


def load_repos(
    repos_file: t.Union[str, os.PathLike] = ".massgit/repos.json",
) -> t.Sequence[Repo]:
    with open(repos_file, mode="r", encoding="utf-8") as fp:
        repos = json.load(fp)

    for repo in repos:
        if "dirname" not in repo:
            repo["dirname"] = repo["url"].removesuffix(".git").rsplit("/", 2)[-1]
            repo["dirname_is_default"] = True
        else:
            repo["dirname_is_default"] = False

    return repos
