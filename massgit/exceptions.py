import typing as t


class GitExitWithNonZeroException(Exception):
    stderr: t.Optional[str]

    def __init__(self, stderr: t.Optional[str] = None):
        self.stderr = stderr
