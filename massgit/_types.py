import typing as t


class Repo(t.TypedDict):
    url: t.Optional[str]
    dirname: t.Optional[str]  # NotRequired
    dirname_is_default: bool
    markers: t.List[str]


class RepoOrigin(t.TypedDict):
    url: t.Optional[str]
    dirname: t.Optional[str]  # NotRequired
    markers: t.Optional[t.List[str]]  # NotRequired
