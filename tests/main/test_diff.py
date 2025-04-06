import sys

from massgit import main
from tests.utils.init import create_massgit_dir
from tests.utils.mock import mock_run


def test__diff(capfd, tmp_cwd):
    create_massgit_dir(tmp_cwd)

    mock_stdout = """diff --git a/build.gradle.kts b/build.gradle.kts
index 70f897e..1489a09 100644
--- a/build.gradle.kts
+++ b/build.gradle.kts
@@ -36,3 +36,5 @@ compose.desktop {
         }
     }
 }
+
+// a
"""
    mock_stderr = "b\n"

    expected_stdout = "repo1:\n" + mock_stdout + "\n"

    args = ["diff"]
    with mock_run(
        "git",
        "diff",
        stdout=mock_stdout,
        stderr=mock_stderr,
        side_effect=lambda: print("b", file=sys.stderr),
    ):
        main(args)
    out, err = capfd.readouterr()
    assert out == expected_stdout
    assert err == mock_stderr
