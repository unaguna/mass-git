import dataclasses
import json
import os
from pathlib import Path
import typing as t

from ._git_process import get_remote_url
from ._types import RepoOrigin, GitExitWithNonZeroException


@dataclasses.dataclass
class InitializeResult:
    massgit_dir: str
    no_url_dirs: t.Sequence[str]


def initialize(
    *,
    basedir: t.Optional[str] = ".",
    massgit_dir_name: t.Optional[str] = None,
    git_dir_name: t.Optional[str] = None,
    repos_filename: str = "repos.json",
) -> InitializeResult:
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
    no_url_dirs: t.List[str] = []
    for git_dir in Path(basedir).rglob(git_dir_name):
        dirname = git_dir.relative_to(basedir).parent
        try:
            url = get_remote_url("origin", dirname, basedir=basedir)
        except GitExitWithNonZeroException:
            no_url_dirs.append(dirname)
            url = None

        repos.append({"url": url, "dirname": dirname})

    with open(os.path.join(massgit_dir, repos_filename), mode="w") as fp:
        json.dump(repos, fp=fp, indent=2, default=str)

    return InitializeResult(
        massgit_dir=str(massgit_dir),
        no_url_dirs=no_url_dirs,
    )
