import typing as t

from ._params import Params
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
    )


def mgclone(
    repos: t.Sequence[Repo],
    *,
    basedir: t.Optional[str] = None,
    git: str = "git",
    env: t.Union[t.Mapping[str, str]] = None,
) -> int:
    exit_codes = []
    # TODO: repos が空の場合の処理

    for repo in repos:
        try:
            _mgclone_each_repo(repo, basedir=basedir, git=git, env=env)
            print(f"clone {repo['dirname']} completed.")
            exit_codes.append(0)
        except _InnerException as e:
            print(f"clone {repo['dirname']} failed: " + e.msg)
            exit_codes.append(1)
        except Exception as e:
            print(f"clone {repo['dirname']} failed: {type(e).__name__} {e}")
            exit_codes.append(1)

    return max(exit_codes)


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
