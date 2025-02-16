import typing as t

from .._types import Repo
from .._repo import load_repos
from ._params import Params
import massgit._git_process as gitproc


def grep_cmd(params: Params) -> int:
    repos = load_repos(params.repos_file)
    return grep(
        repos,
        params.remaining_args,
        basedir=params.basedir,
        git=params.git_exec_path,
        env=params.env,
    )


def grep(
    repos: t.Sequence[Repo],
    args: t.Sequence[str] = tuple(),
    *,
    basedir: t.Optional[str] = None,
    git: str = "git",
    env: t.Union[t.Mapping[str, str]] = None,
) -> int:
    found_flg = False
    exit_codes_err = []
    for repo in repos:
        res = gitproc.trap_stdout(
            "grep",
            repo,
            args,
            basedir=basedir,
            git=git,
            env=env,
        )

        if res.returncode in (0, 1):
            if res.returncode == 0:
                found_flg = True
            for line in res.stdout.split("\n"):
                if len(line) <= 0:
                    continue
                print(repo["dirname"], line)
        else:
            exit_codes_err.append(res.returncode)
            print(repo["dirname"] + f": failed ({res.returncode})")

    if len(exit_codes_err) > 0:
        return max(exit_codes_err)
    elif found_flg:
        return 0
    else:
        return 1
