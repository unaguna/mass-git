import ast
import typing as t
from collections import defaultdict
from types import CodeType


class MarkerProcessor:
    _compiled_marker_condition: CodeType

    def __init__(self, marker_condition: t.Union[str, ast.Expression]):
        if isinstance(marker_condition, str):
            marker_condition = ast.parse(marker_condition, mode="eval")

        # TODO: 想定しない構文の場合に例外を発する
        self._compiled_marker_condition = compile(marker_condition, "<marker>", "eval")

    def accept(self, markers: t.Sequence[str]) -> bool:
        globals_d = {
            # exec, eval 等ビルトイン関数を使用不可にするため、ビルトイン機能を明示する
            "__builtins__": {},
        }
        locals_d = defaultdict(lambda: False, **{m: True for m in markers})
        return eval(self._compiled_marker_condition, globals_d, locals_d)


class AcceptAnyMarkerProcessor(MarkerProcessor):
    def __init__(self):
        super().__init__("True")
