import typing as t


class Repo(t.TypedDict):
    url: t.Optional[str]
    dirname: t.Optional[str]  # NotRequired
    dirname_is_default: bool


class RepoOrigin(t.TypedDict):
    url: t.Optional[str]
    dirname: t.Optional[str]  # NotRequired


class GitExitWithNonZeroException(Exception):
    pass
