import typing as t


class Repo(t.TypedDict):
    url: str
    dirname: t.Optional[str]  # NotRequired
    dirname_is_default: bool
