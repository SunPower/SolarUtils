@ECHO OFF

REM Configure SDK7 Environment
REM **************************

REM %PROGRAMFILES% is expanded to "Program Files" so use quotes around spaces
SET SETENV="%PROGRAMFILES%\Microsoft SDKs\Windows\v7.0\Bin\SetEnv.cmd"

REM Start a new CMD shell
REM Enable command extensions
REM Enable delayed environment variable expansion
REM Shell remains
REM Set SDK environment
REM Targeting Windows 7 x64 RELEASE
%COMSPEC% /E:ON /V:ON /K %SETENV% /RELEASE /X64
