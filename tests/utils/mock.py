import contextlib
import re
import subprocess
import typing as t
from unittest.mock import MagicMock


class CmdMatch(t.NamedTuple):
    cmd: str
    match: str = ".*"
    result_code: int = 0
    stdout: str = ""
    stderr: str = ""
    side_effect: t.Callable = None


@contextlib.contextmanager
def mock_run(*cmd_match: t.Union[str, CmdMatch], **kws):
    # https://stackoverflow.com/questions/25692440/mocking-a-subprocess-call-in-python

    sub_run = subprocess.run
    mock = MagicMock()
    if isinstance(cmd_match[0], str):
        cmd_match = [CmdMatch(*cmd_match, **kws)]

    def new_run(cmd, **_kws):
        check_cmd = " ".join(cmd[1:])
        mock(*cmd[1:])
        for m in cmd_match:
            if m.cmd in cmd[0].lower() and re.match(m.match, check_cmd):
                if m.side_effect:
                    m.side_effect()
                return subprocess.CompletedProcess(
                    cmd, m.result_code, m.stdout, m.stderr
                )
        assert False, "No matching call for %s" % check_cmd

    subprocess.run = new_run
    yield mock
    subprocess.run = sub_run
