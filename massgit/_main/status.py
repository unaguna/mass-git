import typing as t

import massgit._git_process as gitproc
from ._params import Params
from .._utils.text import tail
from .._repo import load_repos, repo_dirname
from .._types import Repo


def status_cmd(params: Params):
    repos = load_repos(params.repos_file)
    status(repos, params.remaining_args, basedir=params.basedir)


def status(
    repos: t.Sequence[Repo],
    args: t.Sequence[str] = tuple(),
    *,
    basedir: t.Optional[str] = None,
):
    for repo in repos:
        dirname = repo_dirname(repo)
        res = gitproc.status(repo, args, basedir=basedir)

        if res.returncode == 0:
            for line in res.stdout.split("\n"):
                if len(line) <= 0:
                    continue
                print(dirname, line)
        else:
            print(dirname, f"failed ({res.returncode})", end="")
            tail_stderr = tail(res.stderr)
            if tail_stderr is not None:
                print(";", tail_stderr)
            else:
                print()
