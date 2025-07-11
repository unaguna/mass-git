from .._logging import get_logger as _get_logger
import copy
import json
import logging
import logging.config
import os
import typing as t


logger = _get_logger("cmd")


class CmdLogFormatter(logging.Formatter):
    _remove_traceback: bool

    def __init__(self, *args, remove_traceback: bool = False, **kwargs):
        super().__init__(*args, **kwargs)
        self._remove_traceback = remove_traceback

    def format(self, record):
        custom_record = copy.copy(record)

        custom_record.levelname = record.levelname.lower()
        if custom_record.msg == "" and custom_record.exc_info:
            e_clz, e, _ = custom_record.exc_info
            custom_record.msg = f"{e_clz.__name__}: {e}"
        if self._remove_traceback:
            custom_record.exc_info = None
            custom_record.exc_text = None
            custom_record.stack_info = None
        message = logging.Formatter.format(self, custom_record)
        if custom_record.name.startswith("massgit"):
            message = "massgit: " + message
        return message


def apply_default_logging_config():
    root_logger = logging.getLogger()
    root_logger.setLevel("WARNING")
    root_logger.addHandler(logging.NullHandler())

    handler = logging.StreamHandler()
    handler.setLevel("WARNING")
    handler.formatter = CmdLogFormatter(
        "%(levelname)s: %(message)s", remove_traceback=True
    )
    logger.addHandler(handler)


def apply_stderr_logging_config(level: str, traceback: bool):
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.formatter = CmdLogFormatter(
        "%(levelname)s: %(message)s", remove_traceback=not traceback
    )
    root_logger.addHandler(handler)


def apply_logging_config_file(config_file: t.Union[str, os.PathLike]):
    # まずエラー出力を設定する。
    # dictConfig 適用中のエラーも出力できるようにするために、この段階で実施する。
    handler = logging.StreamHandler()
    handler.setLevel("WARNING")
    handler.formatter = CmdLogFormatter(
        "%(levelname)s: %(message)s", remove_traceback=True
    )
    logger.addHandler(handler)

    # apply the logging configuration file
    try:
        import yaml

        with open(config_file, mode="rt") as fp:
            config = yaml.load(fp, yaml.Loader)
    except ModuleNotFoundError:
        with open(config_file, mode="rt") as fp:
            config = json.load(fp)
    logging.config.dictConfig(config)

    # dictConfig によってエラー出力が上書きされた場合に備えて、再度エラー出力を設定する。
    # ただし、明示的に disable_existing_loggers=True が指定されている場合は上書きがユーザの意思であると判断して、再設定はしない。
    if not config.get("disable_existing_loggers", False):
        logger.removeHandler(handler)
        logger.addHandler(handler)
