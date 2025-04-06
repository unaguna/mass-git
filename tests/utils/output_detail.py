import typing as t

from tests.utils.resources import DefMockSubproc


class OutputDetail:
    """the object to print details of pytest into stdout"""

    def mock(self, mock: DefMockSubproc):
        print()
        print("--mock--")
        mock.pprint()

    def res(self, *, out: t.Optional[str], err: t.Optional[str]):
        print()
        print("--stdout--")
        if out is not None:
            print(out)
        else:
            print("(None)")
        print()
        print("--stderr--")
        if err is not None:
            print(err)
        else:
            print("(None)")
