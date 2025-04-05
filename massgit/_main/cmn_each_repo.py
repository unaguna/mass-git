import typing as t

from .subcmd import SubCmd
from .._types import Repo
from .._repo import load_repos
from ._params import Params
import massgit._git_process as gitproc


def cmn_each_repo_cmd2(
    subcmd: SubCmd,
    params: Params,
    remaining_args: t.Sequence[str],
) -> int:
    repos = load_repos(params.repos_file)
    return cmn_each_repo(
        subcmd,
        repos,
        remaining_args,
        basedir=params.basedir,
        git=params.git_exec_path,
        env=params.env,
    )


def cmn_each_repo(
    subcmd: SubCmd,
    repos: t.Sequence[Repo],
    args: t.Sequence[str] = tuple(),
    *,
    basedir: t.Optional[str] = None,
    git: str = "git",
    env: t.Union[t.Mapping[str, str]] = None,
) -> int:
    exit_codes = []
    for repo in repos:
        res = gitproc.trap_stdout(
            subcmd.name(),
            repo,
            args,
            basedir=basedir,
            git=git,
            env=env,
        )
        exit_codes.append(res.returncode)

        if res.returncode == 0:
            subcmd.subprocess_result_processor(args=args).print_stdout(
                res.returncode, res.stdout, dirname=repo["dirname"]
            )
        else:
            print(
                repo["dirname"] + f": failed ({res.returncode})",
                file=subcmd.file_to_output_fail_msg(args),
            )

    return subcmd.summarize_exit_code(exit_codes)
