@echo off
setlocal

REM バッチファイル自身が存在するディレクトリパスを取得
set "bin_dir=%~dp0"
set "bin_dir=%bin_dir:~0,-1%"
set "root_dir=%bin_dir%\.."
set "script_dir=%root_dir%\etc"


REM 環境変数 PYTHONPATH に親ディレクトリを指定
set "PYTHONPATH=%root_dir%"

REM 仮想環境のディレクトリを指定
set "venv_dir=%script_dir%\.venv"
set "python_venv=%venv_dir%\Scripts\python.exe"

REM 仮想環境が存在しない場合は作成する
if not exist "%venv_dir%" (
    echo Creating virtual environment...
    python -m venv --upgrade-deps "%venv_dir%"
    "%python_venv%" -m pip install -r "%script_dir%\requirements.txt"
)

REM massgit を実行
"%python_venv%" -m massgit %*
