import pytest

from massgit import main
from tests.utils.init import create_massgit_dir
from tests.utils.mock import captured_stdouterr


@pytest.mark.parametrize(
    ("mock_def", "env_text"),
    [
        ("0_cmn_env/change_git_command", "MASSGIT_GIT=dummy_git"),
        ("0_cmn_env/change_git_command", "MASSGIT_GIT = dummy_git"),
        ("0_cmn_env/change_git_command", "DUMMY=dummy\nMASSGIT_GIT=dummy_git"),
        ("0_cmn_env/change_git_command", "#DUMMY=dummy\nMASSGIT_GIT=dummy_git"),
        ("0_cmn_env/change_git_command", "# DUMMY=dummy\nMASSGIT_GIT=dummy_git"),
        ("0_cmn_env/change_git_command", 'MASSGIT_GIT="dummy_git"'),
        ("0_cmn_env/change_git_command", 'MASSGIT_GIT = "dummy_git"'),
        ("0_cmn_env/change_git_command", "MASSGIT_GIT='dummy_git'"),
        ("0_cmn_env/change_git_command", "MASSGIT_GIT = 'dummy_git'"),
        # ignore comment-out lines
        ("0_cmn_env/default", "#MASSGIT_GIT=dummy_git"),
        ("0_cmn_env/default", "#MASSGIT_GIT = dummy_git"),
        ("0_cmn_env/default", "# MASSGIT_GIT=dummy_git"),
        ("0_cmn_env/default", "DUMMY=dummy\n#MASSGIT_GIT=dummy_git"),
        ("0_cmn_env/default", "DUMMY=dummy\n# MASSGIT_GIT=dummy_git"),
    ],
)
def test__install_dir_env__change_git_command(
    mock_subprocess,
    mock_sep,
    tmp_cwd,
    tmp_config_dir,
    resources,
    output_detail,
    mock_def,
    env_text,
):
    def_mock_subproc = resources.load_mock_subproc(mock_def)
    output_detail.mock(def_mock_subproc)
    create_massgit_dir(tmp_cwd, dirnames=def_mock_subproc.repo_dirnames())

    mock_subprocess(def_mock_subproc)

    # write .env
    with open(tmp_config_dir.joinpath(".env"), mode="w") as fp:
        print(env_text, file=fp)

    with captured_stdouterr() as capout:
        actual_exit_code = main(
            def_mock_subproc.input_args, install_config_dir=tmp_config_dir
        )
    out, err = capout.readouterr()
    output_detail.res(out=out, err=err)
    assert actual_exit_code == def_mock_subproc.expected_result_code
    assert out == def_mock_subproc.expected_stdout
    assert err == def_mock_subproc.expected_stderr
