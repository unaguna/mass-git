import ast
import typing as t
from collections import defaultdict
from types import CodeType


def marker_expression(value: str) -> ast.Expression:
    marker_condition = ast.parse(value, mode="eval")

    # TODO: 想定しない構文の場合に例外を発する

    return marker_condition


class MarkerProcessor:
    _compiled_marker_condition: CodeType

    def __init__(self, marker_condition: t.Union[str, ast.Expression]):
        if isinstance(marker_condition, str):
            marker_condition = marker_expression(marker_condition)

        self._compiled_marker_condition = compile(marker_condition, "<marker>", "eval")

    def accept(self, markers: t.Sequence[str]) -> bool:
        globals_d = {
            # exec, eval 等ビルトイン関数を使用不可にするため、ビルトイン機能を明示する
            "__builtins__": {},
        }
        locals_d = defaultdict(lambda: False, **{m: True for m in markers})
        return eval(self._compiled_marker_condition, globals_d, locals_d)

    def iter_accepted(
        self, items: t.Iterable[t.Any], marker: t.Callable[[t.Any], t.Sequence[str]]
    ):
        for item in items:
            if self.accept(marker(item)):
                yield item


class AcceptAnyMarkerProcessor(MarkerProcessor):
    def __init__(self):
        super().__init__("True")
