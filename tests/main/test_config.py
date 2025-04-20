import pytest

from massgit import main
from tests.utils.init import create_massgit_dir
from tests.utils.mock import captured_stdouterr


@pytest.mark.parametrize(
    ("mock_def",),
    [
        ("config/1repo",),
        ("config/2repo",),
        ("config/one_config",),
        ("config/some_error",),
    ],
)
def test__config(
    mock_subprocess, mock_sep, tmp_cwd, resources, output_detail, mock_def
):
    def_mock_subproc = resources.load_mock_subproc(mock_def)
    output_detail.mock(def_mock_subproc)
    create_massgit_dir(tmp_cwd, dirnames=def_mock_subproc.repo_dirnames())

    mock_subprocess(def_mock_subproc)

    with captured_stdouterr() as capout:
        actual_exit_code = main(def_mock_subproc.input_args)
    out, err = capout.readouterr()
    output_detail.res(out=out, err=err)
    assert actual_exit_code == def_mock_subproc.expected_result_code
    assert out == def_mock_subproc.expected_stdout
    assert err == def_mock_subproc.expected_stderr
