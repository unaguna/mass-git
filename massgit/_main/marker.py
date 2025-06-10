import typing as t


class MarkerProcessor:
    _markers: t.Sequence[str]

    def __init__(self, marker_condition_args: t.Sequence[str]):
        self._markers = tuple(
            part for marker in marker_condition_args for part in marker.split()
        )

    def __contains__(self, item: str) -> bool:
        if not isinstance(item, str):
            return False

        return item in self._markers
