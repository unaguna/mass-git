import os
import subprocess
import sys
import typing as t

from ._types import Repo
from ._repo import repo_dirname


def clone(
    repo: Repo,
    *,
    git: str = "git",
    basedir: t.Optional[str] = None,
    encoding: str = sys.getdefaultencoding(),
) -> int:
    res = subprocess.run(
        [git, "clone", repo["url"]],
        stderr=subprocess.DEVNULL,
        encoding=encoding,
        cwd=basedir,
    )
    return res.returncode


def checkout(
    repo: Repo,
    args: t.Sequence[str] = tuple(),
    *,
    git: str = "git",
    basedir: t.Optional[str] = None,
    encoding: str = sys.getdefaultencoding(),
) -> subprocess.CompletedProcess[str]:
    res = subprocess.run(
        [git, "checkout", *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding=encoding,
        cwd=os.path.join(basedir or "", repo_dirname(repo)),
    )
    return res


def start(cmd: t.Sequence[str]):
    with subprocess.Popen(cmd) as proc:
        pass
        # for line in proc.stdout:
        #     print(line)
