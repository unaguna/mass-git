import typing as t

from .._types import Repo
from .._repo import load_repos
from ._params import Params
import massgit._git_process as gitproc


def cmn_each_repo_cmd(subcmd: str, params: Params):
    repos = load_repos(params.repos_file)
    branch(
        subcmd,
        repos,
        params.remaining_args,
        basedir=params.basedir,
    )


def branch(
    subcmd: str,
    repos: t.Sequence[Repo],
    args: t.Sequence[str] = tuple(),
    *,
    basedir: t.Optional[str] = None,
):
    for repo in repos:
        res = gitproc.trap_stdout(
            subcmd,
            repo,
            args,
            basedir=basedir,
        )
        if res.returncode == 0:
            stdout_trimmed = res.stdout.strip()
            if stdout_trimmed.count("\n") <= 0:
                print(repo["dirname"] + ":", stdout_trimmed)
            else:
                print(repo["dirname"])
                print(res.stdout)
        else:
            print(repo["dirname"] + f": failed ({res.returncode})")
