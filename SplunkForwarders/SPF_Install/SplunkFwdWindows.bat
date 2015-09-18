@echo off
setlocal

REM : User Configurable Variables
set SplunkUFBuild=6.2.6
set LogDir=C:\BuildLogs\
set LogFile=SplunkUniversalForwarderInstall.log
set LogPath=%LogDir%%LogFile%
set productSN=SplunkUF

REM : ================================= ======================================
REM : DO NOT Amend anything below 
REM : ================================= ======================================
if not exist %LogDir% mkdir %LogDir%

IF "%PROCESSOR_ARCHITECTURE%" == "AMD64" goto b64
IF "%PROCESSOR_ARCHITEW6432%" == "AMD64" goto b64

:b32
set SPLUNK_MSI=splunkforwarder-%SplunkUFBuild%-x86-release.msi
REM set above path to 32-bit version
goto endb6432
 
:b64
set SPLUNK_MSI=splunkforwarder-%SplunkUFBuild%-x64-release.msi
REM set above path to 64-bit version
 
:endb6432
 
if not defined ProgramFilesW6432 (
    set LOC=%ProgramFiles%\SplunkUniversalForwarder
) else (
    set LOC=%ProgramFilesW6432%\SplunkUniversalForwarder
)

echo %date%-%time% Product="%productSN%" Build="%SplunkUFBuild%" Message="File Validation" Status="VALIDATE" FileName="%SPLUNK_MSI%" >> "%LogPath%"
echo Installing Splunk...
echo %date%-%time% Product="%productSN%" Build="%SplunkUFBuild%" Message="MSI_Install" Status="START" >> "%LogPath%"
msiexec.exe /i "%SPLUNK_MSI%" INSTALLDIR="%LOC%" AGREETOLICENSE=Yes LAUNCHSPLUNK=0 /QUIET

set msierror=%errorlevel%
if %msierror%==0 goto :InstallSuccess
if %msierror%==1641 goto :InstallSuccess
if %msierror%==3010 goto :InstallSuccess
 
goto :InstallError
 
:InstallSuccess
echo %date%-%time% Product="%productSN%" Build="%SplunkUFBuild%" Message="MSI_Install" Status="DONE" ErrorCode="%msierror%" >> "%LogPath%"
goto :StartConfig
 
:InstallError
echo %date%-%time% Product="%productSN%" Build="%SplunkUFBuild%" Message="MSI_Install" Status="ERROR" ErrorCode="%msierror%" >> "%LogPath%"
goto :EndScript
:StartConfig
echo Copying over custom configuration...
echo %date%-%time% Product="%productSN%" Build="%SplunkUFBuild%" Message="Copy_configuration" Status="START" >> "%LogPath%"
xcopy "%~dp0\etc" "%LOC%\etc" /s /f /y /r

IF %ERRORLEVEL% NEQ 0 (
echo %date%-%time% Product="%productSN%" Build="%SplunkUFBuild%" Message="Failed to Copy Configs" Status="FAILED" ErrorCode="%ERRORLEVEL%" >> "%LogPath%"
goto :EndScript
) ELSE (
echo %date%-%time% Product="%productSN%" Build="%SplunkUFBuild%" Message="Copy_configuration" Status="DONE" ErrorCode="%ERRORLEVEL%" >> "%LogPath%"
)

pushd "%LOC%\bin"
echo Starting Splunk...
echo %date%-%time% Product="%productSN%" Build="%SplunkUFBuild%" Message="Starting UF" Status="START" >> "%LogPath%"
splunk start splunkd --accept-license --no-prompt --answer-yes
echo %date%-%time% Product="%productSN%" Build="%SplunkUFBuild%" Message="Starting UF" Status="DONE" >> "%LogPath%"

echo %date%-%time% Product="%productSN%" Build="%SplunkUFBuild%" Message="SplunkUF Installed & Configured Successfully" Status="COMPLETE" >> "%LogPath%"

popd
endlocal
@echo on

:EndScript
echo Exit Code: %msierror% 
