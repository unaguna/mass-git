import typing as t

from .._types import Repo
from .._repo import repo_dirname
import massgit._git_process as gitproc


def clone(repos: t.Sequence[Repo], *, basedir: t.Optional[str] = None):
    for repo in repos:
        print("clone", repo_dirname(repo) + " ", end="")
        return_code = gitproc.clone(repo, basedir=basedir)
        if return_code == 0:
            print("done")
        else:
            print(f"failed ({return_code})")
