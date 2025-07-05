import typing as t

from ._logging import logger
from ._params import Params
from .marker import MarkerProcessor, AcceptAnyMarkerProcessor
from .._repo import load_repos
from .._types import Repo
from ..exceptions import GitExitWithNonZeroException
import massgit._git_process as gitproc


def mgclone_cmd(params: Params) -> int:
    repos = load_repos(params.repos_file)
    return mgclone(
        repos,
        basedir=params.basedir,
        git=params.git_exec_path,
        env=params.env,
        marker_processor=params.marker_processor,
    )


def mgclone(
    repos: t.Sequence[Repo],
    *,
    basedir: t.Optional[str] = None,
    git: str = "git",
    env: t.Union[t.Mapping[str, str]] = None,
    marker_processor: MarkerProcessor = AcceptAnyMarkerProcessor(),
) -> int:
    exit_codes = []

    for repo in marker_processor.iter_accepted(repos, lambda r: r["markers"]):
        try:
            _mgclone_each_repo(repo, basedir=basedir, git=git, env=env)
            print(f"clone {repo['dirname']} completed.")
            exit_codes.append(0)
        except _InnerException as e:
            print(f"clone {repo['dirname']} failed: " + e.msg.strip())
            exit_codes.append(1)
        except Exception as e:
            print(f"clone {repo['dirname']} failed: {type(e).__name__} {e}")
            exit_codes.append(1)

    if len(exit_codes) <= 0:
        logger.warning(
            "The operation was performed on NO repos. Please refer repos.json and markers."
        )

    return max(exit_codes) if len(exit_codes) > 0 else 0


def _mgclone_each_repo(
    repo: Repo,
    *,
    basedir: t.Optional[str] = None,
    git: str = "git",
    env: t.Union[t.Mapping[str, str]] = None,
) -> int:
    repo_url = repo.get("url")
    if repo_url is None:
        raise _InnerException("URL is not specified")

    try:
        gitproc.clone(
            repo["url"],
            repo["dirname"],
            basedir=basedir,
            git=git,
            env=env,
        )
    except GitExitWithNonZeroException as e:
        raise _InnerException(e.stderr) from e

    return 0


class _InnerException(Exception):
    msg: str

    def __init__(self, msg: str):
        self.msg = msg
