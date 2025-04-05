import os
import typing as t
from argparse import ArgumentParser

from .cmn_each_repo import cmn_each_repo_cmd2
from .massinit import massinit_cmd
from .._utils.dotenv import load_dotenv
from ._params import Params
from .checkout import checkout_cmd
from .clone import clone_cmd
from .diff import diff_cmd
from .subcmd import BranchCmd, ConfigCmd, FetchCmd, GrepCmd, PullCmd, StatusCmd

subcmd_list = [ConfigCmd(), GrepCmd(), StatusCmd(), BranchCmd(), FetchCmd(), PullCmd()]
subcmds = {cmd.name(): cmd for cmd in subcmd_list}


def main(
    argv: t.Sequence[str],
    *,
    install_config_dir: str,
    cwd_config_dir: str = ".massgit",
) -> int:
    parser = ArgumentParser(prog="massgit")
    subparsers = parser.add_subparsers(dest="subcmd", required=True)

    subparsers.add_parser("clone", help="Clone repositories into new directories")
    subparsers.add_parser(
        "massinit",
        help="Initialize massgit",
    )
    subparsers.add_parser(
        "checkout",
        help="Switch branches or restore working tree files",
    )
    for cmd in subcmd_list:
        subparsers.add_parser(
            cmd.name(),
            help=cmd.help(),
        )
    parser_diff = subparsers.add_parser(
        "diff",
        help="Show changes between commits, commit and working tree, etc",
    )
    parser_diff.add_argument("--shortstat", action="store_true")
    parser_diff.add_argument("--show-no-change", action="store_true")
    parser_diff.add_argument("--name-only", action="store_true")

    main_args, remaining_args = parser.parse_known_args(argv)

    dotenv_pub = load_dotenv(
        os.path.join(install_config_dir, ".env"), empty_if_non_exist=True
    )
    dotenv_cwd = load_dotenv(
        os.path.join(cwd_config_dir, ".env"), empty_if_non_exist=True
    )
    env = {**os.environ, **dotenv_pub, **dotenv_cwd}

    if main_args.subcmd in subcmds:
        params = Params(main_args, env, cwd_config_dir=cwd_config_dir)
        exit_code = cmn_each_repo_cmd2(
            subcmds[main_args.subcmd], params, remaining_args
        )
    elif main_args.subcmd == "clone":
        params = Params(
            main_args, None, remaining_args, env, cwd_config_dir=cwd_config_dir
        )
        exit_code = clone_cmd(params)
    elif main_args.subcmd == "massinit":
        params = Params(
            main_args, None, remaining_args, env, cwd_config_dir=cwd_config_dir
        )
        exit_code = massinit_cmd(params)
    elif main_args.subcmd == "checkout":
        params = Params(
            main_args, None, remaining_args, env, cwd_config_dir=cwd_config_dir
        )
        exit_code = checkout_cmd(params)
    elif main_args.subcmd == "diff":
        sub_args, sub_remaining_args = parser_diff.parse_known_args(remaining_args)
        params = Params(
            main_args, sub_args, sub_remaining_args, env, cwd_config_dir=cwd_config_dir
        )
        exit_code = diff_cmd(params)
    else:
        raise Exception()

    return exit_code
