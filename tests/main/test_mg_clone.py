import pytest

from massgit import main
from tests.utils.init import create_massgit_dir
from tests.utils.mock import captured_stdouterr


@pytest.mark.parametrize(
    ("mock_def",),
    [
        ("mg_clone/1repo",),
        ("mg_clone/2repo",),
        ("mg_clone/some_error",),
        ("mg_clone/some_exception",),
    ],
)
def test__mg_clone(
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

    mocked_subproc = mock_subprocess(def_mock_subproc, trap_stderr=True)

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


@pytest.mark.parametrize(
    ("mock_def",),
    [
        ("mg_clone/some_no_url",),
    ],
)
def test__mg_clone__error_with_no_url(
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
    massgit_dir = create_massgit_dir(
        tmp_cwd,
        repos=[{"dirname": "repo1"}, *def_mock_subproc.repos()],
        no_url_dirnames={"repo1"},
    )
    output_detail.json_file(massgit_dir.repos_path, name="repos.json")

    mocked_subproc = mock_subprocess(def_mock_subproc, trap_stderr=True)

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


def test__mg_clone__error_with_unknown_cmd_option(
    mock_subprocess,
    mock_sep,
    tmp_cwd,
    tmp_config_dir,
    resources,
    output_detail,
):
    mock_def = "mg_init/error_with_unknown_option"
    def_mock_subproc = resources.load_mock_subproc(mock_def)
    output_detail.mock(def_mock_subproc)
    create_massgit_dir(tmp_cwd, repos=[{"dirname": "repo1"}])

    mocked_subproc = mock_subprocess(def_mock_subproc, trap_stderr=True)

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
