import typing as t

from ._params import Params
from ..initialize import initialize, MassgitAlreadyInitialized


def massinit_cmd(params: Params) -> int:
    return massinit(
        basedir=params.basedir,
        massgit_dir_name=params.massgit_dir,
    )


def massinit(
    *,
    basedir: t.Optional[str] = None,
    massgit_dir_name: t.Optional[str] = None,
) -> int:
    try:
        result = initialize(
            basedir=basedir or ".",
            massgit_dir_name=massgit_dir_name,
        )
    except MassgitAlreadyInitialized as e:
        print(f"massgit initialization failed: already initialized: {e}")
        return 1

    if len(result.no_url_dirs) > 0:
        for dirname in result.no_url_dirs:
            print(f"WARN: cannot register url of '{dirname}' because get-url is failed")

    print("massgit is initialized:", result.massgit_dir)
    return 0
