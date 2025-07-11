import typing as t

from ._logging import logger
from .marker import MarkerProcessor, AcceptAnyMarkerProcessor
from .subcmd import WrapGitSubCmd
from .._types import Repo
from .._repo import load_repos
from ._params import Params
import massgit._git_process as gitproc


def cmn_each_repo_cmd2(
    subcmd: WrapGitSubCmd,
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
        rep_suffix=params.rep_suffix,
        marker_processor=params.marker_processor,
    )


def cmn_each_repo(
    subcmd: WrapGitSubCmd,
    repos: t.Sequence[Repo],
    args: t.Sequence[str] = tuple(),
    *,
    basedir: t.Optional[str] = None,
    git: str = "git",
    env: t.Union[t.Mapping[str, str]] = None,
    rep_suffix: t.Optional[str] = None,
    marker_processor: MarkerProcessor = AcceptAnyMarkerProcessor(),
) -> int:
    rep_suffix_err = rep_suffix if rep_suffix is not None else ": "
    exit_codes = []
    for repo in marker_processor.iter_accepted(repos, lambda r: r["markers"]):
        try:
            res = gitproc.trap_stdout(
                subcmd.name(),
                repo,
                args,
                basedir=basedir,
                git=git,
                env=env,
            )
        except Exception as e:
            logger.error(
                "failed to run '%s %s ...' for repo '%s'",
                git,
                subcmd.name(),
                repo["dirname"],
                exc_info=e,
            )
            exit_codes.append(129)
            continue

        try:
            exit_codes.append(res.returncode)

            if subcmd.exit_code_is_no_error(res.returncode):
                subcmd.subprocess_result_processor(
                    args=args, rep_suffix=rep_suffix
                ).print_stdout(res.returncode, res.stdout, dirname=repo["dirname"])
            else:
                print(
                    repo["dirname"],
                    rep_suffix_err,
                    f"failed ({res.returncode})",
                    file=subcmd.file_to_output_fail_msg(args),
                    sep="",
                )
        except Exception as e:
            logger.error(
                "failed to output result of '%s %s ...' for repo '%s'",
                git,
                subcmd.name(),
                repo["dirname"],
                exc_info=e,
            )
            exit_codes.append(129)
            continue

    if len(exit_codes) <= 0:
        logger.warning(
            "The operation was performed on NO repos. Please refer repos.json and markers."
        )

    return subcmd.summarize_exit_code(exit_codes)
