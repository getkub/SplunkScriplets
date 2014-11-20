REM #################################################################
REM # If possible Install SplunkForwarders with admin permissions
REM # "Splunk Fowarder" Command Line installation for Windows Server
REM # The script aims to install forwarders and point to a deployment server
REM # All configuration is then done at Master deployment server
REM #################################################################

set installable="E:\installables\splunkforwarder-6.2-x64-release.msi"
set dep_server="1.2.3.4:8089"
set installDir="E:\Program Files\SplunkUniversalForwarder"
set SPLUNKD_PORT="8089"

msiexec.exe /I  %installable% AGREETOLICENSE=Yes INSTALLDIR=%installDir% DEPLOYMENT_SERVER=%dep_server% SPLUNKD_PORT=%SPLUNKD_PORT%  SERVICESTARTTYPE=auto  LAUNCHSPLUNK=1 /quiet

REM # The command prompt will return quickly, but it might be still installing
REM # Wait for 5 minutes
REM # Later verify by running "E:\Program Files\SplunkUniversalForwarder\bin\splunk -version"
