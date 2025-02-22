import os
import typing as t

from .._types import Repo
from .._repo import load_repos
from ._params import Params
import massgit._git_process as gitproc


def diff_cmd(params: Params) -> int:
    repos = load_repos(params.repos_file)
    return diff(
        repos,
        params.remaining_args,
        basedir=params.basedir,
        is_shortstat=params.is_shortstat,
        show_no_change=params.show_no_change,
        name_only=params.name_only,
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
    name_only: bool = False,
    git: str = "git",
    env: t.Union[t.Mapping[str, str]] = None,
) -> int:
    exit_codes = []
    for repo in repos:
        res = gitproc.diff(
            repo,
            args,
            basedir=basedir,
            is_shortstat=is_shortstat,
            name_only=name_only,
            git=git,
            env=env,
        )
        exit_codes.append(res.returncode)

        if res.returncode == 0:
            stdout_trimmed = res.stdout.strip()
            if show_no_change or len(stdout_trimmed) > 0:
                if is_shortstat:
                    print(repo["dirname"] + ":", stdout_trimmed or "0 files changed")
                elif name_only:
                    for line in stdout_trimmed.split("\n"):
                        line_stripped = line.strip()
                        if len(line_stripped) > 0:
                            print(repo["dirname"] + os.sep + line_stripped)
                else:
                    print(repo["dirname"])
                    print(res.stdout)
        else:
            print(repo["dirname"] + f": failed ({res.returncode})")

    return max(exit_codes)
