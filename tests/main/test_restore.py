import pytest

from massgit import main
from tests.utils.init import create_massgit_dir
from tests.utils.mock import captured_stdouterr


@pytest.mark.parametrize(
    ("mock_def",),
    [
        ("restore/1repo",),
        ("restore/2repo",),
        ("restore/some_error",),
        ("restore/some_error_reverse",),
        ("restore/rep_suffix",),
        ("restore/markers",),
    ],
)
def test__restore(
    mock_subprocess,
    mock_sep,
    tmp_cwd,
    tmp_config_dir,
    resources,
    output_detail,
    mock_def,
):
    def_mock_subproc = resources.load_mock_subproc(mock_def)
    output_detail.mock(def_mock_subproc)
    create_massgit_dir(tmp_cwd, repos=def_mock_subproc.repos())

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
