import sys
from argparse import ArgumentParser

from ._params import Params
from .clone import clone_cmd


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcmd")

    parser_clone = subparsers.add_parser(
        "clone", help="Clone repositories into new directories"
    )
    parser_clone.set_defaults()

    args = parser.parse_args(sys.argv[1:])
    params = Params(args)

    if args.subcmd == "clone":
        clone_cmd(params)
    else:
        raise Exception()
