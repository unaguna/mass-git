import typing as t

import massgit._git_process as gitproc
from ._params import Params
from .._utils.text import tail
from .._repo import load_repos
from .._types import Repo


def status_cmd(params: Params) -> int:
    repos = load_repos(params.repos_file)
    return status(
        repos,
        params.remaining_args,
        basedir=params.basedir,
        git=params.git_exec_path,
        env=params.env,
    )


def status(
    repos: t.Sequence[Repo],
    args: t.Sequence[str] = tuple(),
    *,
    basedir: t.Optional[str] = None,
    git: str = "git",
    env: t.Union[t.Mapping[str, str]] = None,
) -> int:
    if "--porcelain" not in args:
        args = ["--porcelain", *args]

    exit_codes = []
    for repo in repos:
        res = gitproc.trap_stdout(
            "status", repo, args, basedir=basedir, git=git, env=env
        )
        exit_codes.append(res.returncode)

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

    return max(exit_codes)
