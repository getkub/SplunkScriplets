@echo off
setlocal
PUSHD "%~dp0"
REM : User Configurable Variables
set SplunkUFVersion=6.3.1
set SplunkUFBuild=f3e41e4b37b2
set LogDir=C:\BuildLogs\
set LogFile=SplunkUniversalForwarderInstall.log
set LogPath=%LogDir%%LogFile%
set productSN=SplunkUF
set runID=T%RANDOM%

REM : ================================= ======================================
REM : DO NOT Amend anything below 
REM : ================================= ======================================
if not exist %LogDir% mkdir %LogDir%
echo Logs will be written to %LogPath%
REM : =============================================
REM : Determining the domain of the computer
REM : =============================================
echo Determining the domain of the computer
set Env=UNKNOWN
for /f "tokens=2 delims==" %%g IN ('wmic.exe COMPUTERSYSTEM GET DOMAIN /Value ^| find /i "domain"') DO set Domain=%%g

if /I %Domain%==admin.xyz set Env=PROD

echo %date%-%time% runID=%runID% Product="%productSN%" Ver="%SplunkUFVersion%" Message="Environment Validation" Status="VALIDATE" Env="%Env%" >> "%LogPath%"

IF %Env%==UNKNOWN (
echo Unable to Determine Environment. Exiting..
goto :EndScript
)

IF NOT EXIST %Env% (
echo Config directory not exists. Exiting..
echo %date%-%time% runID=%runID% Product="%productSN%" Ver="%SplunkUFVersion%" Message="Config Directory NOT exists for Env" Status="ERROR" Env="%Env%">> "%LogPath%"
goto :EndScript
)
REM : =============================================
REM : Determining PROCESSOR ARCHITECTURE
REM : =============================================
IF "%PROCESSOR_ARCHITECTURE%" == "AMD64" goto b64
IF "%PROCESSOR_ARCHITEW6432%" == "AMD64" goto b64

:b32
set SPLUNK_MSI=splunkforwarder-%SplunkUFVersion%-%SplunkUFBuild%-x86-release.msi
REM set above path to 32-bit version
goto endb6432
 
:b64
set SPLUNK_MSI=splunkforwarder-%SplunkUFVersion%-%SplunkUFBuild%-x64-release.msi
REM set above path to 64-bit version
 
:endb6432
 
if not defined ProgramFilesW6432 (
    set LOC=%ProgramFiles%\SplunkUniversalForwarder
) else (
    set LOC=%ProgramFilesW6432%\SplunkUniversalForwarder
)

REM : =============================================
REM : Uninstall Previous Universal Forwarders
REM : =============================================
echo Un-Installing Previous Splunk Agents if any...
echo %date%-%time% runID=%runID% Product="%productSN%" Ver="%SplunkUFVersion%" Message="wmic_Uninstall" Status="START" >> "%LogPath%"
wmic.exe PRODUCT where name="UniversalForwarder" call uninstall /nointeractive
set msierror=%errorlevel%
if %msierror%==0 goto :UnInstallSuccess
REM : If the uninstall fails, quit further installation
echo %date%-%time% runID=%runID% Product="%productSN%" Ver="%SplunkUFVersion%" Message="wmic_Uninstall" Status="DONE" ErrorCode="%msierror%" >> "%LogPath%"
goto :EndScript

REM : =============================================
REM : Install Splunk Universal Forwarder
REM : =============================================
:UnInstallSuccess
echo %date%-%time% runID=%runID% Product="%productSN%" Ver="%SplunkUFVersion%" Message="wmic_Uninstall" Status="DONE" ErrorCode="%msierror%" >> "%LogPath%"
echo Installing Splunk Agent...
echo %date%-%time% runID=%runID% Product="%productSN%" Ver="%SplunkUFVersion%" Message="MSI_Install" Status="START" >> "%LogPath%"
msiexec.exe /i "%SPLUNK_MSI%" INSTALLDIR="%LOC%" AGREETOLICENSE=Yes LAUNCHSPLUNK=0 /QUIET

set msierror=%errorlevel%
if %msierror%==0 goto :InstallSuccess
if %msierror%==1641 goto :InstallSuccess
if %msierror%==3010 goto :InstallSuccess
 
goto :InstallError

:InstallSuccess
echo %date%-%time% runID=%runID% Product="%productSN%" Ver="%SplunkUFVersion%" Message="MSI_Install" Status="DONE" ErrorCode="%msierror%" >> "%LogPath%"
goto :StartConfig
 
:InstallError
echo %date%-%time% runID=%runID% Product="%productSN%" Ver="%SplunkUFVersion%" Message="MSI_Install" Status="ERROR" ErrorCode="%msierror%" >> "%LogPath%"
goto :EndScript

:StartConfig
REM : =============================================
REM : Copying configurations based on ENV
REM : =============================================
echo Copying over custom configuration...
echo %date%-%time% runID=%runID% Product="%productSN%" Ver="%SplunkUFVersion%" Message="Copy_configuration" Status="START" >> "%LogPath%"
xcopy "%~dp0\%Env%\etc" "%LOC%\etc" /s /f /y /r  >nul

IF %ERRORLEVEL% NEQ 0 (
echo %date%-%time% runID=%runID% Product="%productSN%" Ver="%SplunkUFVersion%" Message="Failed to Copy Configs" Status="FAILED" ErrorCode="%ERRORLEVEL%" >> "%LogPath%"
goto :EndScript
) ELSE (
echo %date%-%time% runID=%runID% Product="%productSN%" Ver="%SplunkUFVersion%" Message="Copy_configuration" Status="DONE" ErrorCode="%ERRORLEVEL%" >> "%LogPath%"
)

find "SPLUNK_BINDIP=127.0.0.1" "%LOC%\etc\splunk-launch.conf" >nul

if %errorlevel% NEQ 0 (
echo %date%-%time% runID=%runID% Product="%productSN%" Ver="%SplunkUFVersion%" Message="Configuring Bind IP" Status="Initialising" ErrorCode="%ERRORLEVEL%" >> "%LogPath%"
echo SPLUNK_BINDIP=127.0.0.1 >> "%LOC%\etc\splunk-launch.conf"
) ELSE (
echo %date%-%time% runID=%runID% Product="%productSN%" Ver="%SplunkUFVersion%" Message="Bind IP already configured" Status="Initialising" ErrorCode="%ERRORLEVEL%" >> "%LogPath%"
)


POPD
pushd "%LOC%\bin"
echo Starting Splunk...
echo %date%-%time% runID=%runID% Product="%productSN%" Ver="%SplunkUFVersion%" Message="Starting UF" Status="START" >> "%LogPath%"
del /Q "%LOC%\etc\system\local\server.conf"
splunk start splunkd --accept-license --no-prompt --answer-yes
echo %date%-%time% runID=%runID% Product="%productSN%" Ver="%SplunkUFVersion%" Message="Starting UF" Status="DONE" >> "%LogPath%"

echo %date%-%time% runID=%runID% Product="%productSN%" Ver="%SplunkUFVersion%" Message="SplunkUF Installed & Configured Successfully" Status="COMPLETE" >> "%LogPath%"


popd

:EndScript
echo Exit Code: %msierror%
exit /b %msierror%
