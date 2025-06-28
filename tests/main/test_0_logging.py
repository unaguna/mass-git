import logging
import os.path

import pytest

from massgit import main
from tests.utils.init import create_massgit_dir
from tests.utils.mock import captured_stdouterr


@pytest.mark.parametrize(
    ("mock_def",),
    [
        ("0_cmn_logging/default_args",),
        ("0_cmn_logging/log_stderr_error",),
        ("0_cmn_logging/log_stderr_info",),
    ],
)
def test__log(
    mock_subprocess,
    mock_sep,
    tmp_cwd,
    tmp_config_dir,
    resources,
    output_detail,
    mock_def,
):
    def_mock_subproc = resources.load_mock_subproc(mock_def)
    output_detail.mock(def_mock_subproc)
    create_massgit_dir(
        tmp_cwd,
        repos=def_mock_subproc.repos(),
    )
    dummy_logger = logging.getLogger("dummy")

    mocked_subproc = mock_subprocess(def_mock_subproc)

    with captured_stdouterr() as capout:
        actual_exit_code = main(
            def_mock_subproc.input_args, install_config_dir=tmp_config_dir
        )
        dummy_logger.error("dummy error message")
    out, err = capout.readouterr()
    output_detail.res(out=out, err=err)
    assert actual_exit_code == def_mock_subproc.expected_result_code
    assert out == def_mock_subproc.expected_stdout
    assert err == def_mock_subproc.expected_stderr
    assert mocked_subproc.assert_call_count()


@pytest.mark.parametrize(
    ("mock_def",),
    [
        ("0_cmn_logging/log_stderr_error_full",),
        ("0_cmn_logging/log_stderr_info_full",),
    ],
)
def test__log__traceback(
    mock_subprocess,
    mock_sep,
    tmp_cwd,
    tmp_config_dir,
    resources,
    output_detail,
    mock_def,
):
    def_mock_subproc = resources.load_mock_subproc(mock_def)
    output_detail.mock(def_mock_subproc)
    create_massgit_dir(
        tmp_cwd,
        repos=def_mock_subproc.repos(),
    )
    dummy_logger = logging.getLogger("dummy")

    mocked_subproc = mock_subprocess(def_mock_subproc)

    with captured_stdouterr() as capout:
        actual_exit_code = main(
            def_mock_subproc.input_args, install_config_dir=tmp_config_dir
        )
        dummy_logger.error("dummy error message")
    out, err = capout.readouterr()
    output_detail.res(out=out, err=err)
    assert actual_exit_code == def_mock_subproc.expected_result_code
    assert out == def_mock_subproc.expected_stdout
    assert (
        def_mock_subproc.expected_stderr + "Traceback (most recent call last):" in err
    )
    assert "Exception: exception for test" in err
    assert "error: dummy error message" in err
    assert mocked_subproc.assert_call_count()


@pytest.mark.parametrize(
    ("log_conf_file",),
    [
        ("log_conf/logging_conf.json",),
        ("log_conf/logging_conf.yaml",),
    ],
)
def test__log__yaml(
    mock_subprocess,
    mock_sep,
    tmp_cwd,
    tmp_config_dir,
    resources,
    output_detail,
    log_conf_file,
):
    mock_def = "0_cmn_logging/log_file"
    def_mock_subproc = resources.load_mock_subproc(mock_def)
    output_detail.mock(def_mock_subproc)
    create_massgit_dir(
        tmp_cwd,
        repos=def_mock_subproc.repos(),
    )
    log_conf_path = resources.use_file(log_conf_file)
    input_args = ["--log", str(log_conf_path), "branch"]
    dummy_logger = logging.getLogger("dummy")

    mocked_subproc = mock_subprocess(def_mock_subproc)

    with captured_stdouterr() as capout:
        actual_exit_code = main(input_args, install_config_dir=tmp_config_dir)
        dummy_logger.error("dummy error message")
    out, err = capout.readouterr()
    output_detail.res(out=out, err=err)
    assert actual_exit_code == def_mock_subproc.expected_result_code
    assert out == def_mock_subproc.expected_stdout
    assert err.startswith(def_mock_subproc.expected_stderr)
    assert mocked_subproc.assert_call_count()


@pytest.mark.parametrize(
    ("log_conf_file",),
    [
        ("log_conf/logging_conf.json",),
        ("log_conf/logging_conf.yaml",),
    ],
)
def test__log__yaml_of_cwd(
    mock_subprocess,
    mock_sep,
    tmp_cwd,
    tmp_config_dir,
    resources,
    output_detail,
    log_conf_file,
):
    mock_def = "0_cmn_logging/log_file"
    def_mock_subproc = resources.load_mock_subproc(mock_def)
    output_detail.mock(def_mock_subproc)
    massgit_dir = create_massgit_dir(
        tmp_cwd,
        repos=def_mock_subproc.repos(),
    )
    resources.use_file(log_conf_file, dest_path=massgit_dir.log_conf_path())
    input_args = ["branch"]
    dummy_logger = logging.getLogger("dummy")

    mocked_subproc = mock_subprocess(def_mock_subproc)

    with captured_stdouterr() as capout:
        actual_exit_code = main(input_args, install_config_dir=tmp_config_dir)
        dummy_logger.error("dummy error message")
    out, err = capout.readouterr()
    output_detail.res(out=out, err=err)
    assert actual_exit_code == def_mock_subproc.expected_result_code
    assert out == def_mock_subproc.expected_stdout
    assert err.startswith(def_mock_subproc.expected_stderr)
    assert mocked_subproc.assert_call_count()


def test__log__args_overwrites_cwd_config(
    mock_subprocess,
    mock_sep,
    tmp_cwd,
    tmp_config_dir,
    resources,
    output_detail,
):
    mock_def = "0_cmn_logging/log_file_args_overwrites_cwd_config"
    def_mock_subproc = resources.load_mock_subproc(mock_def)
    output_detail.mock(def_mock_subproc)
    massgit_dir = create_massgit_dir(
        tmp_cwd,
        repos=def_mock_subproc.repos(),
    )
    # use dummy2 via cwd log conf path
    resources.use_file(
        "log_conf/logging_conf_with_dummy2.yaml", dest_path=massgit_dir.log_conf_path()
    )
    # use dummy1 via option --log
    log_conf_path = resources.use_file("log_conf/logging_conf_with_dummy1.yaml")
    input_args = ["--log", str(log_conf_path), "branch"]
    dummy1_logger = logging.getLogger("dummy1")
    dummy2_logger = logging.getLogger("dummy2")

    mocked_subproc = mock_subprocess(def_mock_subproc)

    with captured_stdouterr() as capout:
        actual_exit_code = main(input_args, install_config_dir=tmp_config_dir)
        dummy1_logger.error("dummy_via_args")
        dummy2_logger.error("dummy_via_cwd_config")
    out, err = capout.readouterr()
    output_detail.res(out=out, err=err)
    assert actual_exit_code == def_mock_subproc.expected_result_code
    assert out == def_mock_subproc.expected_stdout
    assert err == def_mock_subproc.expected_stderr
    assert mocked_subproc.assert_call_count()
    assert os.path.isfile(massgit_dir.log_conf_path())


def test__log__yaml__disable_default(
    mock_subprocess,
    mock_sep,
    tmp_cwd,
    tmp_config_dir,
    resources,
    output_detail,
):
    log_conf_file = "log_conf/logging_conf_disable_default.yaml"
    mock_def = "0_cmn_logging/log_file_disable_default"
    def_mock_subproc = resources.load_mock_subproc(mock_def)
    output_detail.mock(def_mock_subproc)
    create_massgit_dir(
        tmp_cwd,
        repos=def_mock_subproc.repos(),
    )
    log_conf_path = resources.use_file(log_conf_file)
    input_args = ["--log", str(log_conf_path), "branch"]
    dummy_logger = logging.getLogger("dummy")

    mocked_subproc = mock_subprocess(def_mock_subproc)

    with captured_stdouterr() as capout:
        actual_exit_code = main(input_args, install_config_dir=tmp_config_dir)
        dummy_logger.error("dummy error message")
    out, err = capout.readouterr()
    output_detail.res(out=out, err=err)
    assert actual_exit_code == def_mock_subproc.expected_result_code
    assert out == def_mock_subproc.expected_stdout
    assert err == def_mock_subproc.expected_stderr
    assert mocked_subproc.assert_call_count()
