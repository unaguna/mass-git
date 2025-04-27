import json
import os
import sys
import traceback
import typing as t
from pprint import pprint

import pytest

from tests.utils.resources import DefMockSubproc


class OutputDetail:
    """the object to print details of pytest into stdout"""

    def obj(self, name: str, obj: t.Any):
        print()
        print(f"--{name}--")
        pprint(obj)

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

    def exc_info(self, exc_info: pytest.ExceptionInfo):
        print()
        print(f"--exception info ({exc_info.typename})--")
        traceback.print_exception(
            exc_info.type, exc_info.value, exc_info.tb, file=sys.stdout
        )

    def json_file(self, path: t.Union[str, os.PathLike[str]], name: str = "JSON file"):
        print()
        print(f"--{name} ({path})--")
        with open(path) as fp:
            pprint(json.load(fp))
