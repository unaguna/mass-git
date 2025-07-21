import contextlib
import io
import sys
import typing as t


class _CapturedStdouterr:
    _out_ctx: t.ContextManager
    _out: t.Optional[io.BytesIO] = None
    _out_bytes: t.Optional[bytes] = None
    _err_ctx: t.ContextManager
    _err: t.Optional[io.BytesIO] = None
    _err_bytes: t.Optional[bytes] = None

    def __enter__(self):
        self._out_ctx = _captured_stdout()
        self._err_ctx = _captured_stderr()

        self._out = self._out_ctx.__enter__()
        self._err = self._err_ctx.__enter__()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._out is not None:
            self._out_ctx.__exit__(exc_type, exc_val, exc_tb)
        if self._err is not None:
            self._err_ctx.__exit__(exc_type, exc_val, exc_tb)

    def get_stdout(self, *, errors: str = "strict") -> str:
        if self._out_bytes is None:
            self._out_bytes = self._out.getvalue()

        return self._out_bytes.decode(errors=errors)

    def get_stderr(self, *, errors: str = "strict") -> str:
        if self._err_bytes is None:
            self._err_bytes = self._err.getvalue()

        return self._err_bytes.decode(errors=errors)

    def readouterr(self, *, errors: str = "strict") -> t.Tuple[str, str]:
        return self.get_stdout(errors=errors), self.get_stderr(errors=errors)


@contextlib.contextmanager
def _captured_output(stream_name):
    orig_stdout = getattr(sys, stream_name)
    setattr(sys, stream_name, _StringBytesIO())
    try:
        yield getattr(sys, stream_name)
    finally:
        setattr(sys, stream_name, orig_stdout)


def _captured_stdout():
    return _captured_output("stdout")


def _captured_stderr():
    return _captured_output("stderr")


class _StringBytesIO(io.BytesIO):
    _encoding = "utf-8"

    def __init__(self):
        super().__init__()
        self.buffer = self

    def write(self, buffer: t.Union[str, bytes], /):
        if isinstance(buffer, str):
            buffer = buffer.encode(self._encoding)
        super().write(buffer)


# class _StringBytesIO(io.StringIO):
#     def __init__(self):
#         super().__init__()
#         self.buffer = _StringBytesIOBuffer(self)
#
#
# class _StringBytesIOBuffer:
#     _base_io: t.TextIO
#     _encoding: str
#
#     def __init__(self, base_io: t.TextIO, *, encoding: str = "utf-8"):
#         self._base_io = base_io
#         self._encoding = encoding
#
#     def write(self, b: bytes, /) -> int:
#         return self._base_io.write(b.decode(encoding=self._encoding, errors=))


def captured_stdouterr() -> _CapturedStdouterr:
    return _CapturedStdouterr()
