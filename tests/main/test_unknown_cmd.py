import subprocess
from unittest.mock import patch

import pytest

from massgit import main


def test__unknown_sub_cmd(
    fp,
    mock_subprocess,
    mock_sep,
    tmp_cwd,
    tmp_config_dir,
    resources,
    output_detail,
):
    """変数subcmdsに不備があり正しいサブコマンドの動作定義をロードできない場合。

    通常は発生しない。
    """
    import massgit._main.main

    with patch.object(massgit._main.main, "subcmds", dict()):
        with pytest.raises(Exception):
            main(["branch"], install_config_dir=tmp_config_dir)

    assert fp.call_count([fp.any()]) == 0
