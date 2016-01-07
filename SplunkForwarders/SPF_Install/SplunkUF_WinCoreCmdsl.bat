::Stop all splunk services
net stop splunkd
net stop splunkweb
::Remove all splunk versions
start /wait MsiExec.exe /uninstall {60ad9785-709f-4b4d-ac19-91cbe0ab7614} /passive
start /wait MsiExec.exe /uninstall {a7579aaa-db6b-46ce-90ca-d8f553481bcc} /passive
start /wait MsiExec.exe /uninstall {2c0fae08-7c9c-40f9-ba21-82a2aad07f0d} /passive

::Map drive to splunk install path
net use /delete S:
net use S: <map network path of splunk executable>

::Execute installation string, minimal configuration
start /wait msiexec.exe /i S:\splunk-4.0.9-74233-x86-release.msi INSTALLDIR="%ProgramFiles%\Splunk" RBG_LOGON_INFO_USER_CONTEXT=2 IS_NET_API_LOGON_USERNAME="<domain\SplunkServiceUser>" IS_NET_API_LOGON_PASSWORD="<Password>" LAUNCHSPLUNK=0 AUTOSTARTSERVICE_SPLUNKD=1 AUTOSTARTSERVICE_SPLUNKWEB=0 /passive
