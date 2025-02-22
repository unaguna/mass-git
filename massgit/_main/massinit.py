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
    result = initialize(
        basedir=basedir or ".",
    )

    if len(result.no_url_dirs) > 0:
        for dirname in result.no_url_dirs:
            print(f"WARN: cannot register url of '{dirname}' because get-url is failed")

    print("massgit is initialized:", result.massgit_dir)
    return 0
