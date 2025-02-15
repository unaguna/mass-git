import typing as t


def tail(text: str) -> t.Optional[str]:
    tail_stderr = [line for line in text.rsplit("\n", 3) if len(line.strip()) > 0]
    if len(tail_stderr) == 0:
        return None
    else:
        return tail_stderr[-1]
