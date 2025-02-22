import json
import os
from pathlib import Path
import typing as t

from ._types import RepoOrigin


def initialize(
    *,
    basedir: t.Optional[str] = ".",
    massgit_dir_name: t.Optional[str] = None,
    git_dir_name: t.Optional[str] = None,
    repos_filename: str = "repos.json",
) -> str:
    if git_dir_name is None:
        git_dir_name = os.environ.get("GIT_DIR", ".git")
    if massgit_dir_name is None:
        massgit_dir_name = os.environ.get("MASSGIT_DIR", ".massgit")

    if not os.path.exists(basedir):
        raise FileNotFoundError(basedir)

    massgit_dir = os.path.join(basedir, massgit_dir_name)
    if os.path.exists(massgit_dir):
        raise FileExistsError(massgit_dir)
    os.mkdir(massgit_dir)

    repos: t.List[RepoOrigin] = []
    for git_dir in Path(basedir).rglob(git_dir_name):
        dirname = git_dir.relative_to(basedir).parent
        repos.append({"url": "", "dirname": dirname})

    with open(os.path.join(massgit_dir, repos_filename), mode="w") as fp:
        json.dump(repos, fp=fp, indent=2, default=str)

    return str(massgit_dir)
