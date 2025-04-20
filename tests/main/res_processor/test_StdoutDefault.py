import pytest

from tests.utils.mock import captured_stdouterr


@pytest.mark.parametrize(
    ("output_with_empty_stdout", "origin_stdout", "expected_output"),
    [
        ("success", "line1\nline2\n\nline4\n", "repo1:\nline1\nline2\n\nline4\n\n"),
        ("success", "line1\n", "repo1: line1\n"),
        ("success", "", "repo1: success\n"),
    ],
)
def test__arg_output_with_empty_stdout(
    output_detail, output_with_empty_stdout, origin_stdout, expected_output
):
    from massgit._main.res_processor import StdoutDefault

    subproc_result_processor = StdoutDefault(
        output_with_empty_stdout=output_with_empty_stdout,
    )

    with captured_stdouterr() as capout:
        subproc_result_processor.print_stdout(
            exit_code=0, origin_stdout=origin_stdout, dirname="repo1"
        )
    out, err = capout.readouterr()
    output_detail.res(out=out, err=err)
    assert out == expected_output
    assert err == ""
