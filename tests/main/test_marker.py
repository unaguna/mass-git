import pytest

from massgit import main
from tests.utils.init import create_massgit_dir
from tests.utils.mock import captured_stdouterr


@pytest.mark.parametrize(
    ("marker_condition",),
    [
        # syntax error
        ("a b",),
        # invalid syntax tree
        ("exec()",),
        ("lambda x: x",),
        ("if a\n    return 0",),
    ],
)
def test__marker__invalid(
    fp,
    mock_sep,
    tmp_cwd,
    tmp_config_dir,
    resources,
    output_detail,
    marker_condition,
):
    args = ["-m", marker_condition, "branch", "--show-current"]
    create_massgit_dir(tmp_cwd)

    with captured_stdouterr() as capout:
        with pytest.raises(SystemExit) as e_ctx:
            main(args, install_config_dir=tmp_config_dir)
    out, err = capout.readouterr()
    output_detail.res(out=out, err=err)
    assert e_ctx.value.code == 2
    assert out == ""
    assert (
        "massgit: error: argument --marker/-m: invalid marker_expression value" in err
    )
    assert len(fp.calls) == 0
