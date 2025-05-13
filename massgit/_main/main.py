import os
import typing as t
from argparse import ArgumentParser

from .cmn_each_repo import cmn_each_repo_cmd2
from .mgclone import mgclone_cmd
from .mginit import mginit_cmd
from .._utils.dotenv import load_dotenv
from ._params import Params
from .subcmd import (
    BranchCmd,
    CheckoutCmd,
    ConfigCmd,
    FetchCmd,
    GrepCmd,
    PullCmd,
    ShowCmd,
    StatusCmd,
    DiffCmd,
    LsFillsCmd,
)

subcmd_list = [
    ConfigCmd(),
    DiffCmd(),
    GrepCmd(),
    ShowCmd(),
    StatusCmd(),
    CheckoutCmd(),
    BranchCmd(),
    FetchCmd(),
    PullCmd(),
    LsFillsCmd(),
]
subcmds = {cmd.name(): cmd for cmd in subcmd_list}


def main(
    argv: t.Sequence[str],
    *,
    install_config_dir: t.Union[os.PathLike[str], str] = os.path.normpath(
        os.path.join(__file__, "..", "..", "..", "etc")
    ),
    cwd_config_dir: str = ".massgit",
) -> int:
    parser = ArgumentParser(prog="massgit")
    parser.add_argument(
        "--rep-suffix",
        required=False,
        help='The suffix of repository name in output. Default is ": " in almost every subcommand.',
    )
    subparsers = parser.add_subparsers(dest="subcmd", required=True)

    mginit_parser = subparsers.add_parser(
        "mg-init",
        help="Initialize massgit",
    )
    mgclone_parser = subparsers.add_parser(
        "mg-clone",
        help="Clone defined repos",
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
    elif main_args.subcmd == "mg-init":
        params = Params(main_args, env, cwd_config_dir=cwd_config_dir)
        mginit_parser.parse_args(remaining_args)
        exit_code = mginit_cmd(params)
    elif main_args.subcmd == "mg-clone":
        params = Params(main_args, env, cwd_config_dir=cwd_config_dir)
        mgclone_parser.parse_args(remaining_args)
        exit_code = mgclone_cmd(params)
    else:
        # NOT reachable (maybe raised faster)
        raise ValueError("unknown subcmd")

    return exit_code
