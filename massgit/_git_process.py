import subprocess
import typing as t

from ._types import Repo


def clone(
    repo: Repo,
    *,
    git: str = "git",
    basedir: t.Optional[str] = None,
) -> int:
    res = subprocess.run(
        [git, "clone", repo["url"]],
        stderr=subprocess.DEVNULL,
        cwd=basedir,
    )
    return res.returncode


def start(cmd: t.Sequence[str]):
    with subprocess.Popen(cmd) as proc:
        pass
        # for line in proc.stdout:
        #     print(line)
