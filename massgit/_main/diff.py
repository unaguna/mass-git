import typing as t

from .._types import Repo
from .._repo import repo_dirname, load_repos
from ._params import Params
import massgit._git_process as gitproc


def diff_cmd(params: Params):
    repos = load_repos(params.repos_file)
    diff(
        repos,
        params.remaining_args,
        basedir=params.basedir,
        is_shortstat=params.is_shortstat,
    )


def diff(
    repos: t.Sequence[Repo],
    args: t.Sequence[str] = tuple(),
    *,
    basedir: t.Optional[str] = None,
    is_shortstat: bool,
):
    for repo in repos:
        res = gitproc.diff(repo, args, basedir=basedir, is_shortstat=is_shortstat)
        if res.returncode == 0:
            if is_shortstat:
                print(repo_dirname(repo) + ":", res.stdout.strip() or "0 files changed")
            else:
                print(repo_dirname(repo))
                print(res.stdout)
        else:
            print(repo_dirname(repo) + f": failed ({res.returncode})")
