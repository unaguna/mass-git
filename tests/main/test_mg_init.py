import json
import os

import pytest

from massgit import main
from tests.utils.init import create_massgit_dir
from tests.utils.mock import captured_stdouterr


@pytest.mark.parametrize(
    ("mock_def", "repo_list"),
    [
        ("mg_init/1repo", ["repo1"]),
        ("mg_init/2repo", ["repo1", "repo2"]),
    ],
)
def test__mg_init(
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
    # create_massgit_dir(tmp_cwd, dirnames=def_mock_subproc.repo_dirnames())

    # create stubs of git local repository
    for repo in repo_list:
        os.makedirs(tmp_cwd.joinpath(repo, ".git"))

    mocked_subproc = mock_subprocess(def_mock_subproc)

    with captured_stdouterr() as capout:
        actual_exit_code = main(
            def_mock_subproc.input_args, install_config_dir=tmp_config_dir
        )
    out, err = capout.readouterr()
    output_detail.res(out=out, err=err)
    assert actual_exit_code == def_mock_subproc.expected_result_code
    assert out == def_mock_subproc.expected_stdout
    assert err == def_mock_subproc.expected_stderr
    assert mocked_subproc.assert_call_count()

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


def test__mg_init__some_no_url(
    mock_subprocess,
    mock_sep,
    tmp_cwd,
    tmp_config_dir,
    resources,
    output_detail,
):
    mock_def = "mg_init/some_no_url"
    repo_list = ["repo1", "repo2"]
    def_mock_subproc = resources.load_mock_subproc(mock_def)
    output_detail.mock(def_mock_subproc)
    # don't create massgit dir (it is created in main(["mg-init"]))
    # create_massgit_dir(tmp_cwd, dirnames=def_mock_subproc.repo_dirnames())

    # create stubs of git local repository
    for repo in repo_list:
        os.makedirs(tmp_cwd.joinpath(repo, ".git"))

    mocked_subproc = mock_subprocess(def_mock_subproc)

    with captured_stdouterr() as capout:
        actual_exit_code = main(
            def_mock_subproc.input_args, install_config_dir=tmp_config_dir
        )
    out, err = capout.readouterr()
    output_detail.res(out=out, err=err)
    assert actual_exit_code == def_mock_subproc.expected_result_code
    assert out == def_mock_subproc.expected_stdout
    assert err == def_mock_subproc.expected_stderr
    assert mocked_subproc.assert_call_count()

    # assert massgit dir
    massgit_dir = tmp_cwd.joinpath(".massgit")
    repos_file = massgit_dir.joinpath("repos.json")
    assert massgit_dir.is_dir()
    assert repos_file.is_file()
    with open(repos_file) as repos_fp:
        repos = json.load(repos_fp)
    output_detail.obj("repos.json", repos)
    assert repos == [
        {"dirname": "repo1", "url": f"https://dummy.example.com/repo1.git"},
        {"dirname": "repo2", "url": None},
    ]


def test__mg_init__error_when_already_initialized(
    mock_subprocess,
    mock_sep,
    tmp_cwd,
    tmp_config_dir,
    resources,
    output_detail,
):
    mock_def = "mg_init/error_when_already_initialized"
    repo_list = ["repo1", "repo2"]
    def_mock_subproc = resources.load_mock_subproc(mock_def)
    output_detail.mock(def_mock_subproc)
    # create massgit dir (raise conflict to main(["mginit"]))
    create_massgit_dir(tmp_cwd, dirnames=repo_list)

    # create stubs of git local repository
    for repo in repo_list:
        os.makedirs(tmp_cwd.joinpath(repo, ".git"))

    mocked_subproc = mock_subprocess(def_mock_subproc)

    with captured_stdouterr() as capout:
        actual_exit_code = main(["mg-init"], install_config_dir=tmp_config_dir)
    out, err = capout.readouterr()
    output_detail.res(out=out, err=err)
    assert actual_exit_code == def_mock_subproc.expected_result_code
    assert out == def_mock_subproc.expected_stdout
    assert err == def_mock_subproc.expected_stderr
    assert mocked_subproc.assert_call_count()


def test__mg_init__error_with_unknown_cmd_option(
    mock_subprocess,
    mock_sep,
    tmp_cwd,
    tmp_config_dir,
    resources,
    output_detail,
):
    mock_def = "mg_init/error_with_unknown_option"
    repo_list = ["repo1", "repo2"]
    def_mock_subproc = resources.load_mock_subproc(mock_def)
    output_detail.mock(def_mock_subproc)
    # don't create massgit dir (it is created in main(["mg-init"]))
    # create_massgit_dir(tmp_cwd, dirnames=def_mock_subproc.repo_dirnames())

    # create stubs of git local repository
    for repo in repo_list:
        os.makedirs(tmp_cwd.joinpath(repo, ".git"))

    mocked_subproc = mock_subprocess(def_mock_subproc)

    with captured_stdouterr() as capout:
        with pytest.raises(SystemExit) as exc_info:
            main(def_mock_subproc.input_args, install_config_dir=tmp_config_dir)
    output_detail.exc_info(exc_info)
    out, err = capout.readouterr()
    output_detail.res(out=out, err=err)
    assert exc_info.value.code == def_mock_subproc.expected_result_code
    assert out == def_mock_subproc.expected_stdout
    assert err == def_mock_subproc.expected_stderr
    assert mocked_subproc.assert_call_count()
