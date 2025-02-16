import os
import subprocess
import sys
import typing as t

from ._types import Repo


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
        cwd=os.path.join(basedir or "", repo["dirname"]),
    )
    return res


def status(
    repo: Repo,
    args: t.Sequence[str] = tuple(),
    *,
    git: str = "git",
    basedir: t.Optional[str] = None,
    encoding: str = sys.getdefaultencoding(),
) -> subprocess.CompletedProcess[str]:
    res = subprocess.run(
        [git, "status", "--porcelain", *(arg for arg in args if arg != "--porcelain")],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding=encoding,
        cwd=os.path.join(basedir or "", repo["dirname"]),
    )
    return res


def diff(
    repo: Repo,
    args: t.Sequence[str] = tuple(),
    *,
    is_shortstat: bool = False,
    git: str = "git",
    basedir: t.Optional[str] = None,
    encoding: str = sys.getdefaultencoding(),
) -> subprocess.CompletedProcess[str]:
    cmd = [git, "diff"]
    if is_shortstat:
        cmd.append("--shortstat")
    if len(args) > 0:
        cmd.append(*args)
    res = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding=encoding,
        cwd=os.path.join(basedir or "", repo["dirname"]),
    )
    return res


def trap_stdout(
    subcmd: str,
    repo: Repo,
    args: t.Sequence[str] = tuple(),
    *,
    git: str = "git",
    basedir: t.Optional[str] = None,
    encoding: str = sys.getdefaultencoding(),
) -> subprocess.CompletedProcess[str]:
    cmd = [git, subcmd, *args]
    res = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        encoding=encoding,
        cwd=os.path.join(basedir or "", repo["dirname"]),
    )
    return res
