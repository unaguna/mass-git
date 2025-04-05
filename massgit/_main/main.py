import os
import typing as t
from argparse import ArgumentParser

from .cmn_each_repo import cmn_each_repo_cmd2
from .massinit import massinit_cmd
from .._utils.dotenv import load_dotenv
from ._params import Params
from .subcmd import (
    BranchCmd,
    CheckoutCmd,
    CloneCmd,
    ConfigCmd,
    FetchCmd,
    GrepCmd,
    PullCmd,
    StatusCmd,
    DiffCmd,
)

subcmd_list = [
    CloneCmd(),
    ConfigCmd(),
    DiffCmd(),
    GrepCmd(),
    StatusCmd(),
    CheckoutCmd(),
    BranchCmd(),
    FetchCmd(),
    PullCmd(),
]
subcmds = {cmd.name(): cmd for cmd in subcmd_list}


def main(
    argv: t.Sequence[str],
    *,
    install_config_dir: str,
    cwd_config_dir: str = ".massgit",
) -> int:
    parser = ArgumentParser(prog="massgit")
    subparsers = parser.add_subparsers(dest="subcmd", required=True)

    subparsers.add_parser(
        "massinit",
        help="Initialize massgit",
    )
    for cmd in subcmd_list:
        subparsers.add_parser(
            cmd.name(),
            help=cmd.help(),
        )

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
    elif main_args.subcmd == "massinit":
        params = Params(
            main_args, None, remaining_args, env, cwd_config_dir=cwd_config_dir
        )
        exit_code = massinit_cmd(params)
    else:
        raise Exception()

    return exit_code
