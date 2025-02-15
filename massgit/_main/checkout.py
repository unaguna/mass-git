import typing as t

import massgit._git_process as gitproc
from ._params import Params
from .._repo import load_repos, repo_dirname
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
        print(repo_dirname(repo), "checkout", *args, end="")
        res = gitproc.checkout(repo, args, basedir=basedir)

        if res.returncode == 0:
            print(" done", end="")
            tail_stdout = [
                line for line in res.stdout.rsplit("\n", 3) if len(line.strip()) > 0
            ]
            if len(tail_stdout) == 0:
                print()
            else:
                print(";", tail_stdout[-1])
        else:
            print(f" failed ({res.returncode})", end="")
            tail_stderr = [
                line for line in res.stderr.rsplit("\n", 3) if len(line.strip()) > 0
            ]
            if len(tail_stderr) == 0:
                print()
            else:
                print(";", tail_stderr[-1])
