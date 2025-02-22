import typing as t

from ._params import Params
from ..initialize import initialize


def massinit_cmd(params: Params) -> int:
    return massinit(
        basedir=params.basedir,
    )


def massinit(
    *,
    basedir: t.Optional[str] = None,
) -> int:
    massgit_dir = initialize(
        basedir=basedir or ".",
    )
    print("massgit is initialized:", massgit_dir)
    return 0
