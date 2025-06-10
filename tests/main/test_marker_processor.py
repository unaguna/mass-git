import pytest

from massgit._main.marker import MarkerProcessor, AcceptAnyMarkerProcessor


PARAMS_CONTAIN_OR_NOT = (
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


@pytest.mark.parametrize(*PARAMS_CONTAIN_OR_NOT)
def test__marker_processor__contains_or_not(marker_condition_args, markers, result):
    processor = MarkerProcessor(marker_condition_args)
    assert processor.accept(markers) is result


@pytest.mark.parametrize(*PARAMS_CONTAIN_OR_NOT)
def test__marker_processor__contains_all(marker_condition_args, markers, result):
    processor = AcceptAnyMarkerProcessor(marker_condition_args)
    assert processor.accept(markers)
