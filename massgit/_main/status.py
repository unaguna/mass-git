import typing as t

import massgit._git_process as gitproc
from ._params import Params
from .._utils.text import tail
from .._repo import load_repos
from .._types import Repo


def status_cmd(params: Params):
    repos = load_repos(params.repos_file)
    status(
        repos,
        params.remaining_args,
        basedir=params.basedir,
        git=params.git_exec_path,
    )


def status(
    repos: t.Sequence[Repo],
    args: t.Sequence[str] = tuple(),
    *,
    basedir: t.Optional[str] = None,
    git: str = "git",
):
    for repo in repos:
        res = gitproc.status(repo, args, basedir=basedir, git=git)

        if res.returncode == 0:
            for line in res.stdout.split("\n"):
                if len(line) <= 0:
                    continue
                print(repo["dirname"], line)
        else:
            print(repo["dirname"], f"failed ({res.returncode})", end="")
            tail_stderr = tail(res.stderr)
            if tail_stderr is not None:
                print(";", tail_stderr)
            else:
                print()
