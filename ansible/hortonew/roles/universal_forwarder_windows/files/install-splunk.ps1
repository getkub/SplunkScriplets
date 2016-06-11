param (
    [string]$site,
    [string]$installer = "c:\Temp\Splunk\splunkforwarder-6.3.0-aa7d4b1ccb80-x64-release.msi",
    [string]$log = "c:\Temp\Splunk\splunkinstall.log"
)

$splunk_install_file = $installer

switch ($site.ToUpper()) {
    "CORPORATE" {$splunk_deployment_server = "10.10.10.10:8089"}
    "SITE1"     {$splunk_deployment_server = "10.10.10.11:8089"}
    "SITE2"     {$splunk_deployment_server = "10.10.10.12:8089"}
    "SITE3"     {$splunk_deployment_server = "10.10.10.13:8089"}
    default {"-site parameter missing.  Site list: corporate, site1, site2, site3"; exit}
}

& msiexec.exe /qn /Liwem! $log /i $splunk_install_file AGREETOLICENSE=Yes DEPLOYMENT_SERVER=`"$splunk_deployment_server`" INSTALL_SHORTCUT=0 /quiet
