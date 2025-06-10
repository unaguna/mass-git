import pytest

from massgit._main.marker import MarkerProcessor


@pytest.mark.parametrize(
    ("marker_condition_args", "markers", "result"),
    [
        (["mark1 mark2"], ["mark1"], True),
        (["mark1 mark2"], ["mark2"], True),
        (["mark1 mark2"], ["mark1", "mark2"], True),
        (["mark1 mark2"], ["mark1", "mark0"], True),
        (["mark1 mark2"], ["mark0", "mark1"], True),
        (["mark1 mark2"], ["mark0"], False),
        (["mark1 mark2"], ["mark1 "], False),
        (["mark1", "mark2"], ["mark1"], True),
        (["mark1", "mark2"], ["mark2"], True),
        (["mark1", "mark2"], ["mark1", "mark2"], True),
        (["mark1", "mark2"], ["mark1", "mark0"], True),
        (["mark1", "mark2"], ["mark0", "mark1"], True),
        (["mark1", "mark2"], ["mark0"], False),
        (["mark1", "mark2"], ["mark1 "], False),
        (["mark1", "mark2 mark3"], ["mark1"], True),
        (["mark1", "mark2 mark3"], ["mark2"], True),
        (["mark1", "mark2 mark3"], ["mark3"], True),
        (["mark1", "mark2 mark3"], ["mark0"], False),
        (["mark1", "mark2 mark3"], ["mark1 "], False),
    ],
)
def test__marker_processor__contains_or_not(marker_condition_args, markers, result):
    processor = MarkerProcessor(marker_condition_args)
    assert processor.accept(markers) is result
