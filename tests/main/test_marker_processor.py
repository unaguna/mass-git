import pytest

from massgit._main.marker import MarkerProcessor, AcceptAnyMarkerProcessor


PARAMS_CONTAIN_OR_NOT = (
    ("marker_condition", "markers", "result"),
    [
        ("mark1", ["mark1"], True),
        ("mark1", ["mark2"], False),
        ("mark1", ["mark1", "mark2"], True),
        ("not mark1", ["mark1"], False),
        ("not mark1", ["mark2"], True),
        ("not mark1", ["mark1", "mark2"], False),
        ("mark1 or mark2", ["mark1"], True),
        ("mark1 or mark2", ["mark2"], True),
        ("mark1 or mark2", ["mark1", "mark2"], True),
        ("mark1 or mark2", ["mark1", "mark0"], True),
        ("mark1 or mark2", ["mark0", "mark1"], True),
        ("mark1 or mark2", ["mark0"], False),
        ("mark1 or mark2", ["mark1 "], False),
        ("mark1 and mark2", ["mark1"], False),
        ("mark1 and mark2", ["mark2"], False),
        ("mark1 and mark2", ["mark1", "mark2"], True),
        ("mark1 and mark2", ["mark1", "mark0"], False),
        ("mark1 and mark2", ["mark0", "mark1"], False),
        ("mark1 and mark2", ["mark0"], False),
        ("mark1 and mark2", ["mark1 "], False),
        ("mark1 and (mark2 or mark3)", ["mark1"], False),
        ("mark1 and (mark2 or mark3)", ["mark1", "mark2"], True),
        ("mark1 and (mark2 or mark3)", ["mark1", "mark3"], True),
        ("mark1 and (mark2 or mark3)", ["mark2", "mark3"], False),
        ("all(mark1, mark2, mark3)", ["mark0"], False),
        ("all(mark1, mark2, mark3)", ["mark1"], False),
        ("all(mark1, mark2, mark3)", ["mark1", "mark2"], False),
        ("all(mark1, mark2, mark3)", ["mark1", "mark2", "mark3"], True),
        ("any(mark1, mark2, mark3)", ["mark0"], False),
        ("any(mark1, mark2, mark3)", ["mark1"], True),
        ("any(mark1, mark2, mark3)", ["mark1", "mark2"], True),
        ("any(mark1, mark2, mark3)", ["mark1", "mark2", "mark3"], True),
    ],
)


@pytest.mark.parametrize(*PARAMS_CONTAIN_OR_NOT)
def test__marker_processor__contains_or_not(marker_condition, markers, result):
    processor = MarkerProcessor(marker_condition)
    assert processor.accept(markers) is result


@pytest.mark.parametrize(*PARAMS_CONTAIN_OR_NOT)
def test__marker_processor__contains_all(marker_condition, markers, result):
    processor = AcceptAnyMarkerProcessor()
    assert processor.accept(markers)


@pytest.mark.parametrize(
    ("marker_condition",),
    [
        # named expr
        ("(a := b)",),
        # non-boolean operations
        ("a + b",),
        ("a - b",),
        ("-a",),
        ("a in b",),
        # lambda
        ("lambda: a",),
        ("lambda b: a",),
        # IF exp
        ("a if b else c",),
        # list, tuple, set, dict
        ("[a]",),
        ("(a, b)",),
        ("{a}",),
        ("{a:b}",),
        ("[a for a in b]",),
        ("[a for a in b if c]",),
        ("{a for a in b}",),
        ("{a for a in b if c}",),
        ("{a:a for a in b}",),
        ("{a:a for a in b if c}",),
        # generator
        ("(a for a in b)",),
        # await
        ("await any()",),
        # yield
        ("(yield a)",),
        ("(yield from a)",),
        # compare
        ("a<b",),
        # call of unexpected name
        ("dummy()",),
        # f-string
        ("f't{a}'",),
        ("f'{a}'",),
        ("f't'",),
        # attribute
        ("a.b",),
        # subscript, slice
        ("a[1]",),
        ("a['a']",),
        ("a[0:3]",),
        # starred
        ("[*a]",),
        ("(*a,)",),
    ],
)
def test__marker_processor__deny_unexpected_syntax(marker_condition):
    with pytest.raises(ValueError) as e_ctx:
        processor = MarkerProcessor(marker_condition)
    assert "Unexpected syntax node" in str(e_ctx.value)
