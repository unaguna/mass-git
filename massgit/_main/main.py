import os
import sys
from argparse import ArgumentParser

from ._params import Params
from .checkout import checkout_cmd
from .clone import clone_cmd
from .diff import diff_cmd
from .status import status_cmd


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcmd")

    subparsers.add_parser("clone", help="Clone repositories into new directories")
    subparsers.add_parser(
        "checkout",
        help="Switch branches or restore working tree files",
    )
    subparsers.add_parser(
        "status",
        help="Show the working tree status",
    )
    parser_diff = subparsers.add_parser(
        "diff",
        help="Show changes between commits, commit and working tree, etc",
    )
    parser_diff.add_argument("--shortstat", action="store_true")
    parser_diff.add_argument("--show-no-change", action="store_true")

    main_args, remaining_args = parser.parse_known_args(sys.argv[1:])
    env = {**os.environ}

    if main_args.subcmd == "clone":
        params = Params(main_args, None, remaining_args, env)
        clone_cmd(params)
    elif main_args.subcmd == "checkout":
        params = Params(main_args, None, remaining_args, env)
        checkout_cmd(params)
    elif main_args.subcmd == "status":
        params = Params(main_args, None, remaining_args, env)
        status_cmd(params)
    elif main_args.subcmd == "diff":
        sub_args, sub_remaining_args = parser_diff.parse_known_args(remaining_args)
        params = Params(main_args, sub_args, sub_remaining_args, env)
        diff_cmd(params)
    else:
        raise Exception()
