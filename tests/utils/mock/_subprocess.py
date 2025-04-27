from pytest_subprocess import FakeProcess

from ..resources import DefMockSubproc


def mock_subproc(
    def_mock_subproc: DefMockSubproc,
    *,
    fp: FakeProcess,
    trap_stderr: bool = False,
):
    for mock_kwargs in def_mock_subproc.mock_param_iter(trap_stderr=trap_stderr):
        fp.register(**mock_kwargs)
