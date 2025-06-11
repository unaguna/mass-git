import pytest

from massgit._main.marker import MarkerProcessor, AcceptAnyMarkerProcessor


PARAMS_CONTAIN_OR_NOT = (
    ("marker_condition", "markers", "result"),
    [
        ("mark1", ["mark1"], True),
        ("mark1", ["mark2"], False),
        ("mark1", ["mark1", "mark2"], True),
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
