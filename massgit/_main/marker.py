import typing as t


class MarkerProcessor:
    _markers: t.Sequence[str]

    def __init__(self, marker_condition_args: t.Sequence[str]):
        self._markers = tuple(
            part for marker in marker_condition_args for part in marker.split()
        )

    def accept(self, markers: t.Sequence[str]) -> bool:
        return any(marker in self._markers for marker in markers)
