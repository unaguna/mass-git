import pytest

from tests.utils.mock import captured_stdouterr


def test__prop_separator():
    from massgit._main.res_processor import StdoutNameEachLinePrefix

    sep = "r"

    subproc_result_processor = StdoutNameEachLinePrefix(sep=sep)
    assert subproc_result_processor.separator == sep


@pytest.mark.parametrize(
    ("trim_empty_line", "expected_output"),
    [
        (True, "repo1: line1\nrepo1: line2\nrepo1: line4\n"),
        (False, "repo1: line1\nrepo1: line2\nrepo1: \nrepo1: line4\nrepo1: \n"),
    ],
)
def test__arg_trim_empty_line__true(output_detail, trim_empty_line, expected_output):
    from massgit._main.res_processor import StdoutNameEachLinePrefix

    origin_stdout = "line1\nline2\n\nline4\n"

    subproc_result_processor = StdoutNameEachLinePrefix(
        sep=": ", trim_empty_line=trim_empty_line
    )

    with captured_stdouterr() as capout:
        subproc_result_processor.print_stdout(
            exit_code=0, origin_stdout=origin_stdout, dirname="repo1"
        )
    out, err = capout.readouterr()
    output_detail.res(out=out, err=err)
    assert out == expected_output
    assert err == ""
