import sys
from argparse import ArgumentParser

from .clone import clone
from .._repo import load_repos


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcmd")

    parser_clone = subparsers.add_parser(
        "clone", help="Clone repositories into new directories"
    )
    parser_clone.set_defaults()

    args = parser.parse_args(sys.argv[1:])

    repos = load_repos()

    if args.subcmd == "clone":
        clone(repos)
    else:
        raise Exception()
