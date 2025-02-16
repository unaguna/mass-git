import os
import typing as t
from argparse import ArgumentParser

from .._utils.dotenv import load_dotenv
from ._params import Params
from .checkout import checkout_cmd
from .clone import clone_cmd
from .cmn_each_repo_cmd import cmn_each_repo_cmd
from .diff import diff_cmd
from .status import status_cmd


def main(
    argv: t.Sequence[str],
    *,
    install_config_dir: str,
    cwd_config_dir: str = ".massgit",
):
    parser = ArgumentParser(prog="massgit")
    subparsers = parser.add_subparsers(dest="subcmd", required=True)

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
    subparsers.add_parser(
        "branch",
        help="List, create, or delete branches",
    )
    subparsers.add_parser(
        "fetch",
        help="Download objects and refs from another repository",
    )

    main_args, remaining_args = parser.parse_known_args(argv)

    dotenv_pub = load_dotenv(
        os.path.join(install_config_dir, ".env"), empty_if_non_exist=True
    )
    dotenv_cwd = load_dotenv(
        os.path.join(cwd_config_dir, ".env"), empty_if_non_exist=True
    )
    env = {**os.environ, **dotenv_pub, **dotenv_cwd}

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
    elif main_args.subcmd in ("branch", "fetch"):
        params = Params(main_args, None, remaining_args, env)
        cmn_each_repo_cmd(main_args.subcmd, params)
    else:
        raise Exception()
