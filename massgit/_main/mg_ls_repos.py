import sys
import typing as t

from ._logging import logger
from ._params import Params
from .marker import MarkerProcessor, AcceptAnyMarkerProcessor
from .._repo import load_repos
from .._types import Repo
import massgit._git_process as gitproc


def mg_ls_repos_cmd(params: Params) -> int:
    repos = load_repos(params.repos_file)
    return mg_ls_repos(
        repos,
        basedir=params.basedir,
        git=params.git_exec_path,
        env=params.env,
        marker_processor=params.marker_processor,
    )


def mg_ls_repos(
    repos: t.Sequence[Repo],
    *,
    basedir: t.Optional[str] = None,
    git: str = "git",
    env: t.Union[t.Mapping[str, str]] = None,
    marker_processor: MarkerProcessor = AcceptAnyMarkerProcessor(),
) -> int:
    exit_codes = []

    for repo in marker_processor.iter_accepted(repos, lambda r: r["markers"]):
        res = gitproc.trap_stdout(
            "status", repo, ("--short",), git=git, basedir=basedir, env=env
        )
        if res.returncode == 0:
            print(repo["dirname"])
        else:
            logger.error(
                "some error occurred since loading the repo '%s'", repo["dirname"]
            )
        exit_codes.append(res.returncode)

    return max((0, *exit_codes))
