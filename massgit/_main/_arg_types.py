import ast

from .marker import marker_expression as __marker_expression


def marker_expression(value: str) -> ast.Expression:
    try:
        return __marker_expression(value)
    except SyntaxError as e:
        raise ValueError from e
