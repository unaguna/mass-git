def test__load_repos(tmp_path, output_detail):
    from massgit._repo import load_repos

    repos_filepath = tmp_path.joinpath("repos.json")

    with open(repos_filepath, mode="w") as fp:
        print(
            '[{"dirname": "repo1", "url": "http://example.com/dummy.git", "markers": ["mark1"]}]',
            file=fp,
        )

    actual_repos = load_repos(repos_filepath)
    output_detail.obj("repos.json", actual_repos)

    assert actual_repos == [
        {
            "dirname": "repo1",
            "url": "http://example.com/dummy.git",
            "dirname_is_default": False,
            "markers": ["mark1"],
        }
    ]


def test__load_repos__without_url(tmp_path, output_detail):
    from massgit._repo import load_repos

    repos_filepath = tmp_path.joinpath("repos.json")

    with open(repos_filepath, mode="w") as fp:
        print('[{"dirname": "repo1", "markers": ["mark1"]}]', file=fp)

    actual_repos = load_repos(repos_filepath)
    output_detail.obj("repos.json", actual_repos)

    assert actual_repos == [
        {
            "dirname": "repo1",
            "dirname_is_default": False,
            "markers": ["mark1"],
        }
    ]


def test__load_repos__without_dirname(tmp_path, output_detail):
    from massgit._repo import load_repos

    repos_filepath = tmp_path.joinpath("repos.json")

    with open(repos_filepath, mode="w") as fp:
        print(
            '[{"url": "http://example.com/repo1.git", "markers": ["mark1"]}]', file=fp
        )

    actual_repos = load_repos(repos_filepath)
    output_detail.obj("repos.json", actual_repos)

    assert actual_repos == [
        {
            "dirname": "repo1",
            "url": "http://example.com/repo1.git",
            "dirname_is_default": True,
            "markers": ["mark1"],
        }
    ]


def test__load_repos__without_marker(tmp_path, output_detail):
    from massgit._repo import load_repos

    repos_filepath = tmp_path.joinpath("repos.json")

    with open(repos_filepath, mode="w") as fp:
        print(
            '[{"dirname": "repo1", "url": "http://example.com/dummy.git"}]',
            file=fp,
        )

    actual_repos = load_repos(repos_filepath)
    output_detail.obj("repos.json", actual_repos)

    assert actual_repos == [
        {
            "dirname": "repo1",
            "url": "http://example.com/dummy.git",
            "dirname_is_default": False,
            "markers": [],
        }
    ]
