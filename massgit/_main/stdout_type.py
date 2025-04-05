import abc


class StdoutType(abc.ABC):
    @abc.abstractmethod
    def print_stdout(self, origin_stdout: str, dirname: str): ...


class StdoutDefault(StdoutType):
    def print_stdout(self, origin_stdout: str, dirname: str):
        stdout_trimmed = origin_stdout.strip()
        if stdout_trimmed.count("\n") <= 0:
            print(dirname + ":", stdout_trimmed or "done")
        else:
            print(dirname)
            print(origin_stdout)


class StdoutNameEachLinePrefix(StdoutType):
    _sep: str

    def __init__(self, sep: str):
        self._sep = sep

    @property
    def separator(self) -> str:
        return self._sep
