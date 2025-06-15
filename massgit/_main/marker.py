import ast
import copy
import typing as t
from types import CodeType


def marker_expression(value: str) -> ast.Expression:
    marker_condition = ast.parse(value, mode="eval", feature_version=(3, 9))

    # 想定しない構文の場合に例外を発する
    _validate_marker_expression(marker_condition)

    return marker_condition


VALID_BUILTINS = {
    "all": lambda *args: all(args),
    "any": lambda *args: any(args),
}


def _validate_marker_expression(value: ast.AST):
    if isinstance(value, ast.Module):
        for node in value.body:
            _validate_marker_expression(node)
        return
    elif isinstance(value, ast.Expression):
        _validate_marker_expression(value.body)
        return
    elif isinstance(value, ast.UnaryOp):
        _validate_marker_expression(value.op)
        return
    elif isinstance(value, ast.Call):
        if isinstance(value.func, ast.Name) and value.func.id in VALID_BUILTINS.keys():
            return
    elif isinstance(value, (ast.BoolOp, ast.Not, ast.Name, ast.Constant)):
        return

    raise ValueError(f"Unexpected syntax node: {value}")


class MarkerProcessor:
    _compiled_marker_condition: CodeType

    def __init__(self, marker_condition: t.Union[str, ast.Expression]):
        if isinstance(marker_condition, str):
            marker_condition = marker_expression(marker_condition)

        self._compiled_marker_condition = compile(marker_condition, "<marker>", "eval")

    def accept(self, markers: t.Sequence[str]) -> bool:
        globals_d = {
            # exec, eval 等ビルトイン関数を使用不可にするため、ビルトイン機能を明示する
            "__builtins__": copy.copy(VALID_BUILTINS),
        }
        locals_d = _DefaultDict(
            {m: True for m in markers},
            default=False,
            excluding_keys={*VALID_BUILTINS.keys()},
        )
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


class _DefaultDict(t.MutableMapping[str, t.Any]):
    """my defaultdict

    Basically, it behaves the same way as defaultdict.
    However, the keys in excluding_keys are always kept without values.
    """

    _default: t.Any
    _base_dict: t.MutableMapping[str, t.Any]
    _excluding_keys: t.Set[str]

    def __init__(
        self,
        base_dict: t.MutableMapping[str, t.Any],
        default: t.Any,
        excluding_keys: t.Set[str],
    ):
        self._default = default
        self._base_dict = base_dict
        self._excluding_keys = excluding_keys

        for k in self._excluding_keys:
            if k in self._base_dict:
                del self._base_dict[k]

    def __getitem__(self, key, /):
        if key in self._excluding_keys:
            raise KeyError(key)
        elif key in self._base_dict:
            return self._base_dict[key]
        else:
            return self._base_dict.setdefault(key, self._default)

    def __len__(self):
        return len(self._base_dict)

    def __iter__(self):
        return self._base_dict.__iter__()

    def __setitem__(self, key, value, /):
        if key in self._excluding_keys:
            raise KeyError(key)
        else:
            self._base_dict.__setitem__(key, value)

    def __delitem__(self, key, /):
        self._base_dict.__delitem__(key)
