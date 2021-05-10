@echo off
set sshKeyPath=rsa_keys\mt_hq_rsa
set sshPath=C:\cygwin\bin\ssh.exe
set vncviewerPath=tvnviewer.exe

IF %1.==. (
	echo.
    echo No phone IP provided
    call :help
	goto :eof
)
IF "%1" == "-h" (
    call :help
	goto :eof
)

IF "%2" NEQ "" set sshKeyPath=%sshKeyPath%.%2

echo.
For %%A in ("%sshKeyPath%") do set sshKeyFileName=%%~nxA
echo Using ssh key %sshKeyFileName%
echo Using ssh path %sshKeyPath%
IF NOT EXIST %sshKeyPath% (
    call :fail SSH key file %sshKeyFileName% not found
    goto :eof
)

set /a port=(%random% %% 10000) + 10000
echo Using port number %port%

start "%1" /MIN "%sshPath%" -o NumberOfPasswordPrompts=1 -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -l admin -i "%sshKeyPath%" -L %port%:127.0.0.1:5900 %1

echo Waiting for SSH to connect
SETLOCAL ENABLEDELAYEDEXPANSION
FOR /L %%G IN (1,1,30) DO (
	netstat -an | find "TCP" | find /C "%port%" > tmp.numports.txt
	set /p open=<tmp.numports.txt
	IF !open! gtr 0 goto :break
	set open=
	timeout /t 1 /nobreak > NUL
)

:break
del /F tmp.numports.txt
If NOT !open! gtr 0 (
    call :fail "SSH failed to connect. Please check HQ IP, SSH key and phone configuration."
	goto :eof
)

timeout /t 5 /nobreak > NUL
echo.
echo Launching VNCViewer
echo If VNC fails to connect, rerun this script
start "" "%vncviewerPath%" -host=127.0.0.1 -port=%port%
goto :eof

:fail
    echo.
    echo Error: %*
	echo.
	pause
	goto :eof

:help
	echo.
	echo Usage: phonevnc.bat phoneIP [optional hqIP]
	echo If hqIP is not provided, default automation "hq_rsa" is used.
	echo Otherwise "hq_rsa.<hqIP>" is used.
	echo hq_rsa or "hq_rsa.<hqIP>" must be present in shared/testdata/ssh folder.
	echo.
	goto :eof