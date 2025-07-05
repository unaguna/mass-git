import typing as t

from ._logging import logger
from ._params import Params
from ..initialize import initialize, MassgitAlreadyInitialized


def mginit_cmd(params: Params) -> int:
    return mginit(
        basedir=params.basedir,
        massgit_dir_name=params.massgit_dir,
    )


def mginit(
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
        logger.error(
            "massgit initialization failed: already initialized: %s", e, exc_info=e
        )
        return 1

    if len(result.no_url_dirs) > 0:
        for dirname in result.no_url_dirs:
            logger.warning(
                "cannot register url of '%s' because get-url is failed", dirname
            )

    print("massgit is initialized:", result.massgit_dir)
    return 0
