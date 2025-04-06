import pytest
from pytest_subprocess import FakeProcess

from massgit import main
from tests.utils.init import create_massgit_dir


@pytest.mark.parametrize(
    ("mock_def",),
    [
        ("diff/1repo",),
        ("diff/2repo",),
        ("diff/some_found",),
        ("diff/some_found_shortstat",),
        ("diff/some_found_name_only",),
        ("diff/some_error",),
        ("diff/some_error_reverse",),
        ("diff/some_error_shortstat",),
    ],
)
def test__diff(capfd, fp: FakeProcess, mock_sep, tmp_cwd, resources, mock_def):
    with capfd.disabled():
        def_mock_subproc = resources.load_mock_subproc(mock_def)
        create_massgit_dir(tmp_cwd, dirnames=def_mock_subproc.repo_dirnames())

        for mock_kwargs in def_mock_subproc.mock_param_iter():
            fp.register(**mock_kwargs)

    actual_exit_code = main(def_mock_subproc.input_args)
    out, err = capfd.readouterr()
    assert actual_exit_code == def_mock_subproc.expected_result_code
    assert out == def_mock_subproc.expected_stdout
    assert err == def_mock_subproc.expected_stderr
