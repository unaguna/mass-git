import json
import os

import pytest

from massgit.initialize import initialize
from tests.utils.mock import captured_stdouterr


@pytest.mark.parametrize(
    ("mock_def", "repo_list"),
    [
        ("mg_init/1repo", ["repo1"]),
        ("mg_init/2repo", ["repo1", "repo2"]),
    ],
)
def test__initialize__arg_git_dir_name(
    mock_subprocess,
    mock_sep,
    tmp_cwd,
    tmp_config_dir,
    resources,
    output_detail,
    mock_def,
    repo_list,
):
    git_dir_name = "stub_git"
    def_mock_subproc = resources.load_mock_subproc(mock_def)
    output_detail.mock(def_mock_subproc)
    # don't create massgit dir (it is created in main(["mg-init"]))
    # create_massgit_dir(tmp_cwd, repos=def_mock_subproc.repos())

    # create stubs of git local repository
    for repo in repo_list:
        os.makedirs(tmp_cwd.joinpath(repo, git_dir_name))

    mock_subprocess(def_mock_subproc)

    with captured_stdouterr() as capout:
        actual_result = initialize(
            massgit_dir_name=".massgit",
            git_dir_name=git_dir_name,
        )
    out, err = capout.readouterr()
    output_detail.res(out=out, err=err)

    # assert massgit dir
    massgit_dir = tmp_cwd.joinpath(".massgit")
    repos_file = massgit_dir.joinpath("repos.json")
    assert massgit_dir.is_dir()
    assert repos_file.is_file()
    with open(repos_file) as repos_fp:
        repos = json.load(repos_fp)
    output_detail.obj("repos.json", repos)
    assert repos == [
        {"dirname": repo, "url": f"https://dummy.example.com/{repo}.git"}
        for repo in repo_list
    ]


@pytest.mark.parametrize(
    ("mock_def", "repo_list"),
    [
        ("mg_init/1repo", ["repo1"]),
        ("mg_init/2repo", ["repo1", "repo2"]),
    ],
)
def test__initialize__arg_massgit_dir_name_default(
    mock_subprocess,
    mock_sep,
    tmp_cwd,
    tmp_config_dir,
    resources,
    output_detail,
    mock_def,
    repo_list,
):
    def_mock_subproc = resources.load_mock_subproc(mock_def)
    output_detail.mock(def_mock_subproc)
    # don't create massgit dir (it is created in main(["mg-init"]))
    # create_massgit_dir(tmp_cwd, repos=def_mock_subproc.repos())

    # create stubs of git local repository
    for repo in repo_list:
        os.makedirs(tmp_cwd.joinpath(repo, ".git"))

    mock_subprocess(def_mock_subproc)

    with captured_stdouterr() as capout:
        actual_result = initialize()
    out, err = capout.readouterr()
    output_detail.res(out=out, err=err)

    assert actual_result.massgit_dir == ".\\.massgit"

    # assert massgit dir
    massgit_dir = tmp_cwd.joinpath(".massgit")
    repos_file = massgit_dir.joinpath("repos.json")
    assert massgit_dir.is_dir()
    assert repos_file.is_file()
    with open(repos_file) as repos_fp:
        repos = json.load(repos_fp)
    output_detail.obj("repos.json", repos)
    assert repos == [
        {"dirname": repo, "url": f"https://dummy.example.com/{repo}.git"}
        for repo in repo_list
    ]


def test__initialize__error_unexists_basedir(tmp_path):
    basedir = tmp_path.joinpath("dummy")

    with pytest.raises(FileNotFoundError) as e:
        initialize(basedir=basedir)

    assert str(e.value) == str(basedir)
