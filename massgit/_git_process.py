import os
import subprocess
import sys
import typing as t

from ._logging import get_logger
from ._types import Repo
from .exceptions import GitExitWithNonZeroException


logger = get_logger("gitprocess")


def trap_stdout(
    subcmd: str,
    repo: Repo,
    args: t.Sequence[str] = tuple(),
    *,
    git: str = "git",
    basedir: t.Optional[str] = None,
    encoding: str = sys.getdefaultencoding(),
    env: t.Optional[t.Mapping[str, str]] = None,
) -> subprocess.CompletedProcess[str]:
    cmd = [git, subcmd, *args]
    logger.info("run %s", cmd)
    # TODO: grep等でエンコードできないバイト列が出てくるケースを想定し、この段階ではstrへのエンコードを実施しないほうがよい
    res = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        encoding=encoding,
        cwd=os.path.join(basedir or "", repo["dirname"]),
        env=env,
    )
    return res


def get_remote_url(
    name: str,
    repo_dirname: str,
    *,
    git: str = "git",
    basedir: t.Optional[str] = None,
    encoding: str = sys.getdefaultencoding(),
    env: t.Optional[t.Mapping[str, str]] = None,
) -> str:
    cmd = [git, "remote", "get-url", name]
    res = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding=encoding,
        cwd=os.path.join(basedir or "", repo_dirname),
        env=env,
    )

    if res.returncode == 0:
        return res.stdout.strip()
    else:
        raise GitExitWithNonZeroException(res.stderr)


def clone(
    repo_url: str,
    repo_dirname: str,
    *,
    git: str = "git",
    basedir: t.Optional[str] = None,
    encoding: str = sys.getdefaultencoding(),
    env: t.Optional[t.Mapping[str, str]] = None,
):
    cmd = [git, "clone", repo_url, repo_dirname]
    res = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding=encoding,
        cwd=basedir,
        env=env,
    )

    if res.returncode == 0:
        return None
    else:
        raise GitExitWithNonZeroException(res.stderr)
