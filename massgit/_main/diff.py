import typing as t

from .._types import Repo
from .._repo import load_repos
from ._params import Params
import massgit._git_process as gitproc


def diff_cmd(params: Params):
    repos = load_repos(params.repos_file)
    diff(
        repos,
        params.remaining_args,
        basedir=params.basedir,
        is_shortstat=params.is_shortstat,
        show_no_change=params.show_no_change,
        git=params.git_exec_path,
        env=params.env,
    )


def diff(
    repos: t.Sequence[Repo],
    args: t.Sequence[str] = tuple(),
    *,
    basedir: t.Optional[str] = None,
    is_shortstat: bool = False,
    show_no_change: bool = False,
    git: str = "git",
    env: t.Union[t.Mapping[str, str]] = None,
):
    for repo in repos:
        res = gitproc.diff(
            repo,
            args,
            basedir=basedir,
            is_shortstat=is_shortstat,
            git=git,
            env=env,
        )
        if res.returncode == 0:
            stdout_trimmed = res.stdout.strip()
            if show_no_change or len(stdout_trimmed) > 0:
                if is_shortstat:
                    print(repo["dirname"] + ":", stdout_trimmed or "0 files changed")
                else:
                    print(repo["dirname"])
                    print(res.stdout)
        else:
            print(repo["dirname"] + f": failed ({res.returncode})")
