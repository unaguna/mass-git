import abc
import typing as t

from ..stdout_type import StdoutType


class SubCmd(abc.ABC):
    @abc.abstractmethod
    def name(self) -> str: ...

    @abc.abstractmethod
    def help(self) -> t.Optional[str]: ...

    @abc.abstractmethod
    def stdout_type(self, args: t.Sequence[str]) -> StdoutType: ...
