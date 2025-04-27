import json
import os
import typing as t


class _EmptySet:
    def __contains__(self, item):
        return False


def _repo(dirname: str, *, no_url_dirnames: t.Set[str]) -> t.Dict[str, t.Any]:
    repo = {"url": f"http://example.com/{dirname}", "dirname": dirname}

    if dirname in no_url_dirnames:
        del repo["url"]

    return repo


def create_massgit_dir(
    cwd: os.PathLike,
    dirnames: t.Sequence = ("repo1",),
    *,
    repos_path: t.Union[os.PathLike[str], str, None] = None,
    no_url_dirnames: t.Set[str] = _EmptySet(),
):
    if repos_path is None:
        repos_path = os.path.join(cwd, ".massgit", "repos.json")
    os.mkdir(os.path.dirname(repos_path))

    repos = [_repo(dirname, no_url_dirnames=no_url_dirnames) for dirname in dirnames]

    with open(repos_path, mode="w") as fp:
        json.dump(repos, fp)
