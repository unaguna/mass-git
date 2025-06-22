import pytest

from massgit import main
from tests.utils.init import create_massgit_dir
from tests.utils.mock import captured_stdouterr


@pytest.mark.parametrize(
    ("mock_def",),
    [
        ("grep/1repo",),
        ("grep/2repo",),
        ("grep/null_sep",),
        ("grep/some_error",),
        ("grep/some_error_reverse",),
        ("grep/some_found",),
        ("grep/not_found",),
        ("grep/rep_suffix",),
        ("grep/rep_suffix_some_found",),
        ("grep/markers",),
    ],
)
def test__grep(
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


@pytest.mark.parametrize(
    ("cont",),
    [
        ("ＡＢＣ".encode("shift_jis"),),
        ("ＡＢＣ".encode("utf_8"),),
    ],
)
@pytest.mark.skip
# TODO: 現状、gitの出力をエンコードできない場合はあきらめて次のリポジトリへ進む暫定措置をとっている。
# そのため、このテストはスキップする。
def test__grep__contamination_binary(fp, tmp_cwd, tmp_config_dir, output_detail, cont):
    create_massgit_dir(tmp_cwd)
    fp.register(["git", "grep", "abc"], stdout=b"file1:abc\nfile2:abc" + cont + b"\n")

    with captured_stdouterr() as capout:
        actual_exit_code = main(["grep", "abc"], install_config_dir=tmp_config_dir)
    out, err = capout.readouterr()
    output_detail.res(out=out, err=err)
    assert actual_exit_code == 0
    # assert out == def_mock_subproc.expected_stdout
    assert err == ""
    assert fp.call_count(["git", "grep", "abc"]) == 1
    assert len(fp.calls) == 1
