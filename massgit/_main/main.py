import argparse
import os
import typing as t
from argparse import ArgumentParser

from ._arg_types import marker_expression
from ._logging import apply_default_logging_config, apply_stderr_logging_config
from ._params import Params
from .cmn_each_repo import cmn_each_repo_cmd2
from .mg_ls_repos import mg_ls_repos_cmd
from .mgclone import mgclone_cmd
from .mginit import mginit_cmd
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
    MgLsReposCmd,
    WrapGitSubCmd,
)
from .._utils.dotenv import load_dotenv

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
    MgLsReposCmd(),
]
subcmds = {cmd.name(): cmd for cmd in subcmd_list}


def _setup_primary_configuration(args: argparse.Namespace):
    """Setup primary python configuration"""

    # setup logging
    if args.log_stderr:
        if "-full" in args.log_stderr:
            level = args.log_stderr.removesuffix("-full")
            is_full = True
        elif "-" in args.log_stderr:
            raise ValueError(args.log_stderr)
        else:
            level = args.log_stderr
            is_full = False
        apply_stderr_logging_config(level, is_full)
    else:
        apply_default_logging_config()


def _build_main_parser() -> argparse.ArgumentParser:
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
    group_logging = parser.add_mutually_exclusive_group()
    group_logging.add_argument(
        "--log-stderr",
        default=None,
        choices=(
            "ERROR",
            "WARNING",
            "INFO",
            "DEBUG",
            "ERROR-full",
            "WARNING-full",
            "INFO-full",
            "DEBUG-full",
        ),
        help=(
            "output logs of specified level or more stronger into standard error. "
            "If '*-full' is specified, "
            "traceback is also output when an exception occurs, etc."
        ),
    )
    return parser


def main(
    argv: t.Sequence[str],
    *,
    install_config_dir: t.Union[os.PathLike[str], str] = os.path.normpath(
        os.path.join(__file__, "..", "..", "..", "etc")
    ),
    cwd_config_dir: str = ".massgit",
) -> int:
    parser = _build_main_parser()
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

    _setup_primary_configuration(main_args)

    subcmd = subcmds[main_args.subcmd]
    subcmd_parser = subparsers_dict[subcmd.name()]
    if subcmd.parse_sub_args():
        sub_args = subcmd_parser.parse_args(remaining_args)
    else:
        sub_args = None
    subcmd.validate(main_args, sub_args, subparser=subcmd_parser)
    params = Params(main_args, env, cwd_config_dir=cwd_config_dir)

    if subcmd.name() == "mg-init":
        exit_code = mginit_cmd(params)
    elif subcmd.name() == "mg-clone":
        exit_code = mgclone_cmd(params)
    elif subcmd.name() == "mg-ls-repos":
        exit_code = mg_ls_repos_cmd(params)
    elif isinstance(subcmd, WrapGitSubCmd):
        exit_code = cmn_each_repo_cmd2(subcmd, params, remaining_args)
    else:
        # NOT reachable (maybe raised faster)
        raise ValueError("unknown subcmd")

    return exit_code
