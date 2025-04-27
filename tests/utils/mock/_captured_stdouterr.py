import io
from test.support import captured_stdout, captured_stderr
import typing as t


class _CapturedStdouterr:
    _out_ctx: t.ContextManager
    _out: t.Optional[io.StringIO] = None
    _out_txt: t.Optional[str] = None
    _err_ctx: t.ContextManager
    _err: io.StringIO = None
    _err_txt: t.Optional[str] = None

    def __enter__(self):
        self._out_ctx = captured_stdout()
        self._err_ctx = captured_stderr()

        self._out = self._out_ctx.__enter__()
        self._err = self._err_ctx.__enter__()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._out is not None:
            self._out_ctx.__exit__(exc_type, exc_val, exc_tb)
        if self._err is not None:
            self._err_ctx.__exit__(exc_type, exc_val, exc_tb)

    def get_stdout(self) -> str:
        if self._out_txt is None:
            self._out_txt = self._out.getvalue()

        return self._out_txt

    def get_stderr(self) -> str:
        if self._err_txt is None:
            self._err_txt = self._err.getvalue()

        return self._err_txt

    def readouterr(self) -> t.Tuple[str, str]:
        return self.get_stdout(), self.get_stderr()


def captured_stdouterr() -> _CapturedStdouterr:
    return _CapturedStdouterr()
