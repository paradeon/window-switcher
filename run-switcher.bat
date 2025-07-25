@echo off

REM Get the directory of the script itself
SET SCRIPT_DIR=%~dp0

REM echo Script Directory: %SCRIPT_DIR%

REM Define paths relative to the script's location
SET VENV_DIR=%SCRIPT_DIR%
SET SCRIPT_NAME=window-switcher.py
SET SCRIPT_PATH=%SCRIPT_DIR%%SCRIPT_NAME%
SET STDOUT_LOG=%SCRIPT_DIR%stdout.log
SET STDERR_LOG=%SCRIPT_DIR%stderr.log

REM Create the log files if they do not exist
IF NOT EXIST "%STDOUT_LOG%" (type nul > "%STDOUT_LOG%")
IF NOT EXIST "%STDERR_LOG%" (type nul > "%STDERR_LOG%")

REM Command to activate virtual environment and run Python script detached
START "" cmd /c "call %VENV_DIR%\Scripts\activate.bat && python %SCRIPT_PATH% 1>> %STDOUT_LOG% 2>> %STDERR_LOG%"

REM echo Python script is running in the background and detached from the terminal.

