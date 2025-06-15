import argparse
import os
import typing as t
from argparse import ArgumentParser

from .cmn_each_repo import cmn_each_repo_cmd2
from ._arg_types import marker_expression
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
    MgCloneCmd,
    MgInitCmd,
    WrapGitSubCmd,
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
    MgCloneCmd(),
    MgInitCmd(),
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
        "--marker",
        "-m",
        type=marker_expression,
        dest="marker_condition",
        help="Specify target repositories by marker. You can specify boolean expression such as 'marker1 or marker2'.",
    )
    parser.add_argument(
        "--rep-suffix",
        required=False,
        help='The suffix of repository name in output. Default is ": " in almost every subcommand.',
    )
    subparsers = parser.add_subparsers(dest="subcmd", required=True)

    subparsers_dict: t.Dict[str, argparse.ArgumentParser] = {}
    for cmd in subcmd_list:
        p = subparsers.add_parser(
            cmd.name(),
            help=cmd.help(),
        )
        subparsers_dict[cmd.name()] = p

    main_args, remaining_args = parser.parse_known_args(argv)

    dotenv_pub = load_dotenv(
        os.path.join(install_config_dir, ".env"), empty_if_non_exist=True
    )
    dotenv_cwd = load_dotenv(
        os.path.join(cwd_config_dir, ".env"), empty_if_non_exist=True
    )
    env = {**os.environ, **dotenv_pub, **dotenv_cwd}

    subcmd = subcmds[main_args.subcmd]
    subcmd_parser = subparsers_dict[subcmd.name()]
    if subcmd.parse_sub_args():
        sub_args = subcmd_parser.parse_args(remaining_args)
    else:
        sub_args = None
    params = Params(main_args, env, cwd_config_dir=cwd_config_dir)

    if subcmd.name() == "mg-init":
        exit_code = mginit_cmd(params)
    elif subcmd.name() == "mg-clone":
        exit_code = mgclone_cmd(params)
    elif isinstance(subcmd, WrapGitSubCmd):
        exit_code = cmn_each_repo_cmd2(subcmd, params, remaining_args)
    else:
        # NOT reachable (maybe raised faster)
        raise ValueError("unknown subcmd")

    return exit_code
