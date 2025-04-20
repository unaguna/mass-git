def test__load_dotenv__empty_value(tmp_path):
    from massgit._utils.dotenv import load_dotenv

    envdir_path = tmp_path.joinpath(".env")

    with open(envdir_path, mode="w") as fp:
        print("ENV=", file=fp)

    actual = load_dotenv(envdir_path)
    return actual.get("ENV") == ""
