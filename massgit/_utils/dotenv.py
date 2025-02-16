import os
import typing as t


def load_dotenv(
    filepath: t.Union[str, os.PathLike], *, empty_if_non_exist: bool = False
) -> t.Dict[str, str]:
    if empty_if_non_exist and not os.path.exists(filepath):
        return {}

    with open(filepath, mode="r", encoding="utf-8") as fp:
        return {
            key: value
            for key, value in (_key_value_of_line(line) for line in fp)
            if key is not None
        }


def _key_value_of_line(line: str) -> t.Tuple[t.Optional[str], str]:
    line = line.strip()
    if len(line) <= 0 or line[0] == "#":
        return None, ""

    key, value = line.split("=", 1)
    return _trim(key), _trim(value)


def _trim(text: str) -> str:
    # キーや値の前後の空白は削除される。
    text = text.strip()

    if len(text) <= 0:
        return ""
    # シングルクォートかダブルクォートで値を囲まれている場合、その中身をそのまま使う。
    elif text[0] == text[-1] == "'" or text[0] == text[-1] == '"':
        return text[1:-1]
    else:
        return text
