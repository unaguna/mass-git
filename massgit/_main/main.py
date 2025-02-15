import os
import sys
from argparse import ArgumentParser

from ._params import Params
from .checkout import checkout_cmd
from .clone import clone_cmd


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcmd")

    subparsers.add_parser("clone", help="Clone repositories into new directories")
    subparsers.add_parser(
        "checkout",
        help="Switch branches or restore working tree files",
    )

    main_args, remaining_args = parser.parse_known_args(sys.argv[1:])
    env = {**os.environ}

    if main_args.subcmd == "clone":
        params = Params(main_args, remaining_args, env)
        clone_cmd(params)
    elif main_args.subcmd == "checkout":
        params = Params(main_args, remaining_args, env)
        checkout_cmd(params)
    else:
        raise Exception()
