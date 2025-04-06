import json
import os
import typing as t


def create_massgit_dir(cwd: os.PathLike, dirnames: t.Sequence = ("repo1",)):
    repos_path = os.path.join(cwd, ".massgit", "repos.json")
    os.mkdir(os.path.dirname(repos_path))

    repos = [
        {"url": f"http://example.com/{dirname}", "dirname": dirname}
        for dirname in dirnames
    ]

    with open(repos_path, mode="w") as fp:
        json.dump(repos, fp)
