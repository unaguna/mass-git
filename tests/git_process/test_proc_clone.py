import pytest

from massgit.exceptions import GitExitWithNonZeroException
from tests.utils.init import create_massgit_dir
from tests.utils.mock import captured_stdouterr


@pytest.mark.parametrize(
    ("mock_def",),
    [
        ("proc_clone/1repo",),
    ],
)
def test__clone(
    mock_subprocess,
    mock_sep,
    tmp_cwd,
    tmp_config_dir,
    resources,
    output_detail,
    mock_def,
):
    from massgit._git_process import clone

    def_mock_subproc = resources.load_mock_subproc(mock_def)
    output_detail.mock(def_mock_subproc)
    create_massgit_dir(tmp_cwd, dirnames=def_mock_subproc.repo_dirnames())

    mock_subprocess(def_mock_subproc, trap_stderr=True)

    with captured_stdouterr() as capout:
        clone("http://dummy.example.com/repo1.git", "repo1")
    out, err = capout.readouterr()
    output_detail.res(out=out, err=err)
    assert out == ""
    assert err == ""


@pytest.mark.parametrize(
    ("mock_def",),
    [
        ("proc_clone/error",),
    ],
)
def test__clone__error(
    mock_subprocess,
    mock_sep,
    tmp_cwd,
    tmp_config_dir,
    resources,
    output_detail,
    mock_def,
):
    from massgit._git_process import clone

    def_mock_subproc = resources.load_mock_subproc(mock_def)
    output_detail.mock(def_mock_subproc)
    create_massgit_dir(tmp_cwd, dirnames=def_mock_subproc.repo_dirnames())

    mock_subprocess(def_mock_subproc, trap_stderr=True)

    with captured_stdouterr() as capout:
        with pytest.raises(GitExitWithNonZeroException) as exc_info:
            clone("http://dummy.example.com/repo1.git", "repo1")
    output_detail.exc_info(exc_info)
    out, err = capout.readouterr()
    output_detail.res(out=out, err=err)
    assert out == ""
    assert err == ""
    assert str(exc_info.value) == "err\n"
