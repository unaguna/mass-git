import typing as t

from .._types import Repo
from .._repo import load_repos
from ._params import Params
import massgit._git_process as gitproc


def clone_cmd(params: Params):
    repos = load_repos(params.repos_file)
    clone(repos, basedir=params.basedir)


def clone(repos: t.Sequence[Repo], *, basedir: t.Optional[str] = None):
    for repo in repos:
        print(repo["dirname"], "clone", end="")
        return_code = gitproc.clone(repo, basedir=basedir)
        if return_code == 0:
            print(" done")
        else:
            print(f" failed ({return_code})")
