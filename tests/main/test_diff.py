import pytest
from pytest_subprocess import FakeProcess

from massgit import main
from tests.utils.init import create_massgit_dir


@pytest.mark.parametrize(
    ("mock_def",),
    [
        ("diff/1repo",),
        ("diff/2repo",),
    ],
)
def test__diff(capfd, fp: FakeProcess, tmp_cwd, resources, mock_def):
    def_mock_subproc = resources.load_mock_subproc(mock_def)
    create_massgit_dir(tmp_cwd, dirnames=def_mock_subproc.repo_dirnames())

    mock_stderr = "b\n"
    for mock_kwargs in def_mock_subproc.mock_param_iter():
        fp.register(**mock_kwargs)

    args = ["diff"]
    main(args)
    out, err = capfd.readouterr()
    assert out == def_mock_subproc.expected_stdout
    # assert err == mock_stderr
