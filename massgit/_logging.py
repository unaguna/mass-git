import logging


def get_logger(name: str = "") -> logging.Logger:
    if name is None or len(name) == 0:
        logger = logging.getLogger("massgit")
    else:
        logger = logging.getLogger(f"massgit.{name}")

    logger.addHandler(logging.NullHandler())
    return logger
