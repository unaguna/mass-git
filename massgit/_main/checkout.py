import typing as t

import massgit._git_process as gitproc
from ._params import Params
from .._utils.text import tail
from .._repo import load_repos
from .._types import Repo


def checkout_cmd(params: Params):
    repos = load_repos(params.repos_file)
    checkout(repos, params.remaining_args, basedir=params.basedir)


def checkout(
    repos: t.Sequence[Repo],
    args: t.Sequence[str] = tuple(),
    *,
    basedir: t.Optional[str] = None,
):
    for repo in repos:
        print(repo["dirname"], "checkout", *args, end="")
        res = gitproc.checkout(repo, args, basedir=basedir)

        if res.returncode == 0:
            print(" done", end="")
            tail_stdout = tail(res.stdout)
            if tail_stdout is not None:
                print(";", tail_stdout)
            else:
                print()
        else:
            print(f" failed ({res.returncode})", end="")
            tail_stderr = tail(res.stderr)
            if tail_stderr is not None:
                print(";", tail_stderr)
            else:
                print()
