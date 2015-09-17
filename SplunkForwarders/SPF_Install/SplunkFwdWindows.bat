@echo off
setlocal

REM : User Configurable Variables
set SplunkUFBuild="6.2.6"
set LogPath="C:\BuildLogs\SplunkUniversalForwarderInstall.log"

REM : ================================= ======================================
REM : DO NOT Amend anything below 
IF "%PROCESSOR_ARCHITECTURE%" == "AMD64" goto b64
IF "%PROCESSOR_ARCHITEW6432%" == "AMD64" goto b64

:b32
set SPLUNK_MSI=%~dp0\splunkforwarder-%SplunkUFBuild%-x86-release.msi
REM set above path to 32-bit version
goto endb6432
 
:b64
set SPLUNK_MSI=%~dp0\splunkforwarder-%SplunkUFBuild%-x64-release.msi
REM set above path to 64-bit version
 
:endb6432
 
if not defined ProgramFilesW6432 (
    set LOC=%ProgramFiles%\SplunkUniversalForwarder
) else (
    set LOC=%ProgramFilesW6432%\SplunkUniversalForwarder
)
 
echo Installing Splunk...
echo "%date%-%time% Product=SplunkUF Build=%SplunkUFBuild% Action=Install_Started" >> "%LogPath%"
msiexec.exe /i "%SPLUNK_MSI%" INSTALLDIR="%LOC%" AGREETOLICENSE=Yes LAUNCHSPLUNK=0 /QUIET

echo Copying over custom configuration...
echo "%date%-%time% Product=SplunkUF Build=%SplunkUFBuild% Action=Copying_configuration" >> "%LogPath%"
xcopy "%~dp0\etc" "%LOC%\etc" /s /f /y /r
pushd "%LOC%\bin"
echo Starting Splunk...
echo "%date%-%time% Product=SplunkUF Build=%SplunkUFBuild% Action=Starting_SplunkUF" >> "%LogPath%"
splunk start splunkd --accept-license --no-prompt --answer-yes
@echo on
popd
endlocal
